import discord
from discord.ext import commands
from config import DISCORD_CHANNEL_ID
from prophecy_generator import ProphecyGenerator
from logger import logger

class ProphecyBot(commands.Bot):
    def __init__(self):
        # Enable required intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None  # Disable default help command
        )

        self.prophecy_generator = ProphecyGenerator()
        self.last_prophecy_timestamp = None

        # Add commands
        self.add_command(self.prophecy)
        self.add_command(self.insight)

    async def setup_hook(self):
        """Called when the bot is setting up"""
        logger.info("ProphecyBot setup complete")

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'Bot connected as {self.user}')
        logger.info(f'Connected to {len(self.guilds)} guilds')

        for guild in self.guilds:
            logger.info(f"Connected to guild: {guild.name}")
            for channel in guild.text_channels:
                logger.info(f"Found channel: {channel.name} (ID: {channel.id})")

    @commands.command(name='prophecy')
    async def prophecy(self, ctx, theme: str = None):
        """Generate a mystical Web3 prophecy"""
        if ctx.channel.id != DISCORD_CHANNEL_ID:
            return

        try:
            prophecy, timestamp = self.prophecy_generator.generate_prophecy(theme)
            self.last_prophecy_timestamp = timestamp

            embed = discord.Embed(
                title="🔮 Web3 Prophecy",
                description=prophecy,
                color=0xff69b4
            )
            await ctx.send(embed=embed)
            logger.info(f"Prophecy delivered to {ctx.author}")

        except Exception as e:
            logger.error(f"Error generating prophecy: {str(e)}")
            await ctx.send("⚠️ The mystic forces are clouded. Please try again later.")

    @commands.command(name='insight')
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
                title="✨ Mystical Insight",
                description=insight,
                color=0x4a90e2
            )
            await ctx.send(embed=embed)
            logger.info(f"Insight delivered to {ctx.author}")

        except Exception as e:
            logger.error(f"Error generating insight: {str(e)}")
            await ctx.send("⚠️ The mystic forces are unable to provide deeper insights at this time.")