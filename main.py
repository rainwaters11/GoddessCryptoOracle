from discord_handler import ProphetBot
from config import DISCORD_TOKEN
from logger import logger

def main():
    try:
        # Create and run the Discord bot
        bot = ProphetBot()
        logger.info("Starting Web3 Prophet Bot...")
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Critical error in main loop: {str(e)}")
        raise

if __name__ == "__main__":
    main()