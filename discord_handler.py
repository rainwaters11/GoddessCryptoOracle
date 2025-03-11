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
        # Early return if wrong channel
        if ctx.channel.id != DISCORD_CHANNEL_ID:
            logger.debug(f"Ignoring prophecy command in channel {ctx.channel.id}")
            return

        logger.debug(f"Processing prophecy command from {ctx.author} in channel {ctx.channel.id}")

        try:
            prophecy, timestamp = self.prophecy_generator.generate_prophecy(theme)
            self.last_prophecy_timestamp = timestamp

            prophecy_embed = discord.Embed(
                title=f"🔮 Web3 Prophecy {theme.upper() if theme else ''} 🔮",
                description=prophecy,
                color=0xff69b4
            )
            await ctx.send(embed=prophecy_embed)
            logger.info(f"Prophecy delivered to {ctx.author}")

        except Exception as e:
            logger.error(f"Error processing prophecy request: {str(e)}")
            await ctx.send("⚠️ The mystic forces are clouded. Please try again later.")

    @commands.command(name='insight')
    async def insight(self, ctx):
        """Get deeper insight into the last prophecy"""
        if ctx.channel.id != DISCORD_CHANNEL_ID:
            logger.debug(f"Ignoring insight command in channel {ctx.channel.id}")
            return

        if not self.last_prophecy_timestamp:
            await ctx.send("🔮 I need a prophecy to draw insights from. Use `!prophecy` first.")
            return

        try:
            insight = self.prophecy_generator.get_insight(self.last_prophecy_timestamp)
            insight_embed = discord.Embed(
                title="✨ Mystical Insight ✨",
                description=insight,
                color=0x4a90e2
            )
            await ctx.send(embed=insight_embed)
            logger.info(f"Insight delivered to {ctx.author}")

        except Exception as e:
            logger.error(f"Error generating insight: {str(e)}")
            await ctx.send("⚠️ The mystic forces are unable to provide deeper insights at this time.")

class ProphecyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True  # Required for command processing
        super().__init__(command_prefix='!', intents=intents)
        logger.info("ProphecyBot initialized")

    async def setup_hook(self):
        """Called when the bot is setting up"""
        await self.add_cog(ProphecyCog(self))
        logger.info("ProphecyBot setup complete")

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'Bot connected as {self.user}')
        channel = self.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            logger.info(f"Found prophecy channel: #{channel.name}")
            help_embed = discord.Embed(
                title="🔮 Web3 Prophet Bot Commands",
                description="**Available Commands:**\n"
                          "`!prophecy` - Receive a mystical Web3 prophecy\n"
                          "`!insight` - Get deeper insight into the last prophecy",
                color=0xff69b4
            )
            await channel.send(embed=help_embed)
        else:
            logger.error(f"Could not find channel with ID: {DISCORD_CHANNEL_ID}")