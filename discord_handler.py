import discord
from discord.ext import commands
from config import DISCORD_CHANNEL_ID
from prophecy_generator import ProphecyGenerator
from logger import logger

class ProphecyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prophecy_generator = ProphecyGenerator()
        self.last_prophecy_timestamp = None
        logger.info("ProphecyCog initialized")

    @commands.command(name='prophecy')
    async def prophecy(self, ctx, theme: str = None):
        """Generate a mystical Web3 prophecy with optional theme"""
        # Only respond in the designated channel
        if ctx.channel.id != DISCORD_CHANNEL_ID:
            return

        try:
            logger.info(f"Processing prophecy request from {ctx.author} with theme: {theme}")

            # Send channeling message
            channeling_msg = await ctx.send("🔮 **Channeling the mystic forces of Web3...**")

            # Generate prophecy
            prophecy, timestamp = self.prophecy_generator.generate_prophecy(theme)
            self.last_prophecy_timestamp = timestamp

            # Delete channeling message
            await channeling_msg.delete()

            # Send the prophecy with theme indicator if specified
            theme_str = f" [{theme.upper()}]" if theme else ""
            prophecy_embed = discord.Embed(
                title=f"🔮 Web3 Prophecy{theme_str} 🔮",
                description=prophecy,
                color=0xff69b4
            )
            prophecy_embed.set_footer(text="Use !insight to reveal deeper meanings...")

            await ctx.send(embed=prophecy_embed)
            logger.info("Prophecy delivered successfully")

        except Exception as e:
            logger.error(f"Error processing prophecy request: {str(e)}")
            await ctx.send("⚠️ The mystic forces are clouded. Please try again later.")

    @commands.command(name='insight')
    async def insight(self, ctx):
        """Get deeper insight into the last prophecy"""
        if ctx.channel.id != DISCORD_CHANNEL_ID or not self.last_prophecy_timestamp:
            return

        try:
            # Send channeling message
            channeling_msg = await ctx.send("🔮 **Delving deeper into the mystic vision...**")

            # Generate insight
            insight = self.prophecy_generator.get_insight(self.last_prophecy_timestamp)

            # Delete channeling message
            await channeling_msg.delete()

            # Send the insight
            insight_embed = discord.Embed(
                title="✨ Mystical Insight ✨",
                description=insight,
                color=0x4a90e2
            )
            await ctx.send(embed=insight_embed)

        except Exception as e:
            logger.error(f"Error generating insight: {str(e)}")
            await ctx.send("⚠️ The mystic forces are unable to provide deeper insights at this time.")

class ProphetBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

        logger.info("ProphetBot initialized")

    async def setup_hook(self):
        """Called when the bot is setting up"""
        await self.add_cog(ProphecyCog(self))
        logger.info("ProphecyCog added")

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'Bot connected as {self.user}')
        logger.info(f'Connected to {len(self.guilds)} servers')

        # Set up the prophecy channel
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            logger.info(f"Found prophecy channel: #{channel.name}")
            help_embed = discord.Embed(
                title="🔮 Web3 Prophet Bot Commands",
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