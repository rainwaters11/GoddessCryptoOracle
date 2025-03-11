import discord
from config import DISCORD_CHANNEL_ID
from prophecy_generator import ProphecyGenerator
from logger import logger

class ProphetBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.prophecy_generator = ProphecyGenerator()
        self.last_prophecy_timestamp = None

    async def on_ready(self):
        logger.info(f"Bot connected as {self.user}")

    async def on_message(self, message):
        # Don't respond to our own messages
        if message.author == self.user:
            return

        # Only respond in the designated channel
        if message.channel.id != DISCORD_CHANNEL_ID:
            return

        # Process commands
        if message.content.startswith('!prophecy'):
            try:
                # Extract theme if provided
                parts = message.content.split(maxsplit=1)
                theme = parts[1] if len(parts) > 1 else None

                # Generate prophecy
                prophecy, timestamp = self.prophecy_generator.generate_prophecy(theme)
                self.last_prophecy_timestamp = timestamp

                # Create and send embed
                theme_str = f" [{theme.upper()}]" if theme else ""
                prophecy_embed = discord.Embed(
                    title=f"🔮 Web3 Prophecy{theme_str} 🔮",
                    description=prophecy,
                    color=0xff69b4
                )
                prophecy_embed.set_footer(text="Use !insight to reveal deeper meanings...")
                await message.channel.send(embed=prophecy_embed)

            except Exception as e:
                logger.error(f"Error in prophecy command: {str(e)}")
                await message.channel.send("⚠️ The mystic forces are clouded. Please try again later.")

        elif message.content == '!insight':
            if not self.last_prophecy_timestamp:
                await message.channel.send("🔮 No recent prophecies to analyze. Request a prophecy first using `!prophecy`")
                return

            try:
                insight = self.prophecy_generator.get_insight(self.last_prophecy_timestamp)
                insight_embed = discord.Embed(
                    title="✨ Mystical Insight ✨",
                    description=insight,
                    color=0x4a90e2
                )
                await message.channel.send(embed=insight_embed)

            except Exception as e:
                logger.error(f"Error in insight command: {str(e)}")
                await message.channel.send("⚠️ The mystic forces are unable to provide deeper insights at this time.")