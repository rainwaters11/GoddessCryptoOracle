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
        self.context = {}  # Store prophecy context for follow-up questions
        self.themes = {
            'defi': 'Focus on decentralized finance, liquidity pools, yield farming, and financial protocols.',
            'nft': 'Focus on NFTs, digital art, metaverse assets, and blockchain collectibles.',
            'dao': 'Focus on decentralized governance, voting mechanisms, and community coordination.',
            None: 'Provide a general Web3 prophecy about any aspect of the ecosystem.'
        }
        logger.info("ProphecyGenerator initialized with local storage fallback")

    def _get_theme_prompt(self, theme=None):
        """Generate a theme-specific prompt"""
        base_prompt = (
            "You are an ancient AI oracle blessed with the power to foresee the future of Web3. "
            "Your prophecies combine deep crypto knowledge with mystical symbolism. "
            "Keep prophecies concise, under 240 characters, and focus on one specific prediction. "
            "Use metaphors, mystical language, and Web3 terminology."
        )

        if theme and theme.lower() in self.themes:
            return f"{base_prompt} {self.themes[theme.lower()]}"
        return f"{base_prompt} {self.themes[None]}"

    def generate_prophecy(self, theme=None):
        """Generate a mystic Web3 prophecy using OpenAI"""
        try:
            logger.info(f"Generating new prophecy with theme: {theme}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_theme_prompt(theme)
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

            # Store context for follow-up questions
            self.context[timestamp] = {
                'prophecy': prophecy,
                'theme': theme,
                'follow_ups': []
            }

            if stored:
                logger.info(f"Prophecy stored successfully with timestamp {timestamp}")
            else:
                logger.warning("Failed to store prophecy, but continuing with generation")

            return prophecy, timestamp

        except Exception as e:
            logger.error(f"Error generating prophecy: {str(e)}")
            raise Exception(f"Failed to generate prophecy: {str(e)}")

    def get_insight(self, timestamp):
        """Generate additional insight for a previous prophecy"""
        try:
            if timestamp not in self.context:
                return "I cannot recall the prophecy you're referring to. Please request a new prophecy."

            context = self.context[timestamp]
            prophecy = context['prophecy']
            theme = context['theme']

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a mystical oracle providing deeper insights into previous prophecies. Explain the hidden meanings and implications while maintaining a mystical tone. {self.themes[theme] if theme else ''}"
                    },
                    {
                        "role": "user",
                        "content": f"Reveal deeper insights about this prophecy: {prophecy}"
                    }
                ],
                max_tokens=200,
                temperature=0.7
            )

            insight = response.choices[0].message.content.strip()
            context['follow_ups'].append(insight)
            return insight

        except Exception as e:
            logger.error(f"Error generating insight: {str(e)}")
            return "The mystic forces are clouded. I cannot provide further insights at this moment."