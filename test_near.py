import os
import subprocess
import json
from datetime import datetime
from near_handler import NEARHandler
from logger import logger

def verify_near_cli():
    """Verify NEAR CLI installation and basic functionality"""
    try:
        # Check if near-cli is installed
        result = subprocess.run(["near", "--version"], capture_output=True, text=True)
        logger.info(f"NEAR CLI version: {result.stdout.strip()}")

        # Check environment variables
        account = os.getenv("NEAR_ACCOUNT")
        private_key = os.getenv("NEAR_PRIVATE_KEY")
        if not account or not private_key:
            logger.error("Missing required NEAR environment variables")
            return False

        logger.info(f"Using NEAR account: {account}")

        # Check if we can access the NEAR network
        result = subprocess.run(["near", "state", account], capture_output=True, text=True)
        logger.info(f"NEAR account state: {result.stdout if result.returncode == 0 else result.stderr}")

        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error verifying NEAR CLI: {str(e)}")
        return False

def test_near_integration():
    try:
        # First verify NEAR CLI
        logger.info("Verifying NEAR CLI installation...")
        if not verify_near_cli():
            logger.error("NEAR CLI verification failed. Please ensure NEAR CLI is properly installed and credentials are set.")
            logger.info("Testing will continue with local storage fallback...")

        # Initialize NEAR handler
        logger.info("Initializing NEAR handler...")
        near = NEARHandler()

        # Create test prophecy data
        timestamp = int(datetime.now().timestamp())
        test_prophecy = "This is a test prophecy from the Web3 Prophet Bot"

        logger.info(f"Attempting to store prophecy with timestamp {timestamp}")

        # Try to store the prophecy
        store_result = near.store_prophecy(test_prophecy, timestamp)
        if store_result:
            logger.info("Successfully stored prophecy!")

            # Verify if prophecy was stored locally
            if os.path.exists(near.local_storage_path):
                with open(near.local_storage_path, 'r') as f:
                    stored_data = json.load(f)
                    if f"prophecy_{timestamp}" in stored_data:
                        logger.info("Verified prophecy in local storage")
                    else:
                        logger.warning("Prophecy not found in local storage")
        else:
            logger.error("Failed to store prophecy")
            return

        # Try to retrieve the prophecy
        logger.info(f"Attempting to retrieve prophecy with timestamp {timestamp}")
        retrieved_prophecy = near.get_prophecy(timestamp)

        if retrieved_prophecy:
            logger.info(f"Successfully retrieved prophecy: {retrieved_prophecy}")

            # Verify the retrieved prophecy content
            if isinstance(retrieved_prophecy, dict) and retrieved_prophecy.get("text") == test_prophecy:
                logger.info("Retrieved prophecy content matches original")
            else:
                logger.warning("Retrieved prophecy content mismatch")
        else:
            logger.error("Failed to retrieve prophecy")

    except Exception as e:
        logger.error(f"Error during NEAR integration test: {str(e)}")
        logger.exception("Full traceback:")
        raise

if __name__ == "__main__":
    test_near_integration()