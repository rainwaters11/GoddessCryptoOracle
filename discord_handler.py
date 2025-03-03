import discord
from discord.ext import commands
from config import DISCORD_CHANNEL_ID
from prophecy_generator import ProphecyGenerator
from logger import logger

class ProphecyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prophecy_generator = ProphecyGenerator()
        logger.info("ProphecyCog initialized")

    @commands.command(name='prophecy')
    async def prophecy(self, ctx):
        """Generate a mystical Web3 prophecy"""
        # Only respond in the designated channel
        if ctx.channel.id != DISCORD_CHANNEL_ID:
            return

        try:
            logger.info(f"Processing prophecy request from {ctx.author}")

            # Send channeling message
            channeling_msg = await ctx.send("🔮 **Channeling the mystic forces of Web3...**")

            # Generate prophecy
            prophecy = self.prophecy_generator.generate_prophecy()

            # Delete channeling message
            await channeling_msg.delete()

            # Send the prophecy
            await ctx.send(f"🔮 **Web3 Prophecy** 🔮\n{prophecy}")
            logger.info("Prophecy delivered successfully")

        except Exception as e:
            logger.error(f"Error processing prophecy request: {str(e)}")
            await ctx.send("⚠️ The mystic forces are clouded. Please try again later.")

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
            await channel.send("🔮 **Web3 Prophet Bot is online!** 🔮\nUse `!prophecy` to receive a mystical vision.")
        else:
            logger.error(f"Could not find channel with ID: {DISCORD_CHANNEL_ID}")