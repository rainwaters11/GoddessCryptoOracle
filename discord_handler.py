import discord
from discord.ext import commands
from config import DISCORD_CHANNEL_ID
from prophecy_generator import ProphecyGenerator
from logger import logger

class ProphecyBot(commands.Bot):
    def __init__(self):
        # Enable ALL required intents explicitly
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.guild_messages = True
        intents.messages = True
        intents.dm_messages = True

        super().__init__(
            command_prefix='!',
            intents=intents,
            description="Web3 Prophet Bot"
        )

        self.prophecy_generator = ProphecyGenerator()
        self.last_prophecy_timestamp = None
        logger.info("ProphecyBot initialized with all required intents")

        # Register commands
        self.remove_command('help')  # Remove default help command
        self.add_command(self.prophecy)
        self.add_command(self.insight)

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'Bot connected as {self.user}')

        # Send help message to designated channel
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            logger.info(f"Found prophecy channel: #{channel.name}")
            help_embed = discord.Embed(
                title="🔮 Summon the Oracle",
                description=(
                    "**Available Commands:**\n"
                    "`!prophecy` - Receive a mystical Web3 prophecy\n"
                    "`!prophecy defi` - Get a DeFi-focused prophecy\n"
                    "`!prophecy nft` - Get an NFT-focused prophecy\n"
                    "`!prophecy dao` - Get a DAO-focused prophecy\n"
                    "`!insight` - Get deeper insight into the last prophecy"
                ),
                color=0xff69b4
            )
            await channel.send(embed=help_embed)
        else:
            logger.error(f"Could not find channel with ID: {DISCORD_CHANNEL_ID}")

    async def on_message(self, message):
        """Handle incoming messages"""
        if message.author == self.user:
            return

        # Log all message attempts
        logger.info(f"Message received: {message.content} from {message.author} in channel {message.channel.id}")

        # Process commands after logging
        await self.process_commands(message)

    @commands.command(name="prophecy")
    async def prophecy(self, ctx, theme: str = None):
        """Generate a mystical Web3 prophecy"""
        logger.info(f"Prophecy command received from {ctx.author} with theme: {theme}")

        if ctx.channel.id != DISCORD_CHANNEL_ID:
            logger.info(f"Ignoring prophecy command in non-prophecy channel {ctx.channel.id}")
            return

        try:
            prophecy, timestamp = self.prophecy_generator.generate_prophecy(theme)
            self.last_prophecy_timestamp = timestamp

            embed = discord.Embed(
                title=f"🔮 Web3 Prophecy {theme.upper() if theme else ''} 🔮",
                description=prophecy,
                color=0xff69b4
            )
            await ctx.send(embed=embed)
            logger.info(f"Prophecy delivered to {ctx.author}")

        except Exception as e:
            logger.error(f"Error generating prophecy: {str(e)}")
            await ctx.send("⚠️ The mystic forces are clouded. Please try again later.")

    @commands.command(name="insight")
    async def insight(self, ctx):
        """Get deeper insight into the last prophecy"""
        logger.info(f"Insight command received from {ctx.author}")

        if ctx.channel.id != DISCORD_CHANNEL_ID:
            logger.info(f"Ignoring insight command in non-prophecy channel {ctx.channel.id}")
            return

        if not self.last_prophecy_timestamp:
            await ctx.send("🔮 I need a prophecy to draw insights from. Use `!prophecy` first.")
            return

        try:
            insight = self.prophecy_generator.get_insight(self.last_prophecy_timestamp)
            embed = discord.Embed(
                title="✨ Mystical Insight ✨",
                description=insight,
                color=0x4a90e2
            )
            await ctx.send(embed=embed)
            logger.info(f"Insight delivered to {ctx.author}")

        except Exception as e:
            logger.error(f"Error generating insight: {str(e)}")
            await ctx.send("⚠️ The mystic forces are unable to provide deeper insights at this time.")