import discord
from discord.ext import commands
from config import DISCORD_CHANNEL_ID
from prophecy_generator import ProphecyGenerator
from logger import logger

class ProphecyBot(commands.Bot):
    def __init__(self):
        # Initialize with only message content intent
        intents = discord.Intents.none()
        intents.message_content = True
        intents.guilds = True

        super().__init__(
            command_prefix='!',
            intents=intents,
            description="Web3 Prophet Bot"
        )

        self.prophecy_generator = ProphecyGenerator()
        self.last_prophecy_timestamp = None

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

    @commands.command()
    async def prophecy(self, ctx, theme: str = None):
        """Generate a mystical Web3 prophecy"""
        if ctx.channel.id != DISCORD_CHANNEL_ID:
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

    @commands.command()
    async def insight(self, ctx):
        """Get deeper insight into the last prophecy"""
        if ctx.channel.id != DISCORD_CHANNEL_ID:
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