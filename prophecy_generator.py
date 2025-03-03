import json
from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY, MAX_PROPHECY_LENGTH
from logger import logger
from near_handler import NEARHandler

class ProphecyGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-4"  # Using standard GPT-4 model
        self.near_handler = NEARHandler()
        logger.info("ProphecyGenerator initialized with local storage fallback")

    def generate_prophecy(self):
        """Generate a mystic Web3 prophecy using OpenAI"""
        try:
            logger.info("Generating new prophecy...")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an ancient AI oracle blessed with the power to foresee the future of Web3. Your prophecies combine deep crypto knowledge with mystical symbolism. Keep prophecies concise, under 240 characters, and focus on one specific prediction. Use metaphors, mystical language, and Web3 terminology (DeFi, DAOs, NFTs, etc.)."
                    },
                    {
                        "role": "user",
                        "content": "Channel your mystic powers and reveal a prophecy about the future of Web3."
                    }
                ],
                max_tokens=150,
                temperature=0.8
            )

            # Extract and clean up the prophecy text
            prophecy = response.choices[0].message.content.strip()
            logger.info(f"Generated prophecy: {prophecy}")

            # Store prophecy with timestamp
            timestamp = int(datetime.now().timestamp())
            stored = self.near_handler.store_prophecy(prophecy, timestamp)

            if stored:
                logger.info(f"Prophecy stored successfully with timestamp {timestamp}")
            else:
                logger.warning("Failed to store prophecy, but continuing with generation")

            return prophecy

        except Exception as e:
            logger.error(f"Error generating prophecy: {str(e)}")
            raise Exception(f"Failed to generate prophecy: {str(e)}")