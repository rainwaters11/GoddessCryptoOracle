import tweepy
from config import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)
from logger import logger

class TwitterHandler:
    def __init__(self):
        try:
            # Initialize v2 client
            self.client = tweepy.Client(
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
            )
            logger.info("Twitter v2 authentication successful")

        except Exception as e:
            logger.error(f"Twitter authentication failed: {str(e)}")
            raise Exception(f"Failed to initialize Twitter client: {str(e)}")

    def post_tweet(self, content):
        try:
            # Check content length
            if len(content) > 280:
                content = content[:277] + "..."

            # Post tweet using v2 endpoint
            response = self.client.create_tweet(text=content)

            if not response or not response.data:
                raise Exception("No response data received from Twitter API")

            tweet_id = response.data['id']
            logger.info(f"Successfully posted tweet with ID: {tweet_id}")
            return tweet_id

        except tweepy.errors.Forbidden as e:
            error_msg = ("Twitter API error: Your account doesn't have permission to post tweets. "
                      "Please ensure you have elevated access in your Twitter Developer Account. "
                      "Visit https://developer.twitter.com/en/portal/products/elevated to upgrade.")
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"Error posting tweet: {str(e)}")
            raise Exception(f"Failed to post tweet: {str(e)}")