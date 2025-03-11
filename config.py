import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Discord Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = 1345696402696704002  # Fixed channel ID for the prophecy channel

# NEAR Configuration
NEAR_ACCOUNT = os.getenv("NEAR_ACCOUNT")

# Scheduling Configuration
POSTING_INTERVAL_HOURS = int(os.getenv("POSTING_INTERVAL_HOURS", "4"))

# Prophecy Configuration
MAX_PROPHECY_LENGTH = 2000  # Discord message length limit