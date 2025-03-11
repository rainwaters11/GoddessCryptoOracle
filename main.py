from discord_handler import ProphecyBot
from config import DISCORD_TOKEN
from logger import logger

def main():
    try:
        # Create and run the Discord bot
        bot = ProphecyBot()
        logger.info("Starting Web3 Prophet Bot...")
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Critical error starting bot: {str(e)}")
        logger.exception("Full traceback:")
        raise

if __name__ == "__main__":
    main()