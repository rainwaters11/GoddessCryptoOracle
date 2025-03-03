import os
import subprocess
import json
import tempfile
from datetime import datetime
from logger import logger

class NEARHandler:
    def __init__(self):
        self.account = os.getenv("NEAR_ACCOUNT")
        self.private_key = os.getenv("NEAR_PRIVATE_KEY")
        self.local_storage_path = "prophecies.json"
        self.blockchain_enabled = False
        
        # Environment variable to force local storage mode
        self.force_local_storage = os.getenv("FORCE_LOCAL_STORAGE", "true").lower() == "true"

        # Initialize local storage if needed
        if not os.path.exists(self.local_storage_path):
            with open(self.local_storage_path, 'w') as f:
                json.dump({}, f)

        # Skip blockchain setup if we're forcing local storage
        if self.force_local_storage:
            logger.info("FORCE_LOCAL_STORAGE is enabled, using local storage only")
            return
            
        # Try to initialize NEAR connection
        try:
            self._setup_near_account()
            self.blockchain_enabled = True
        except Exception as e:
            logger.warning(f"Failed to initialize NEAR blockchain connection: {str(e)}")
            logger.info("Falling back to local storage")

    def _setup_near_account(self):
        """Setup NEAR account using environment credentials"""
        try:
            # Check if NEAR CLI is in PATH
            which_result = subprocess.run(
                ["which", "near"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info(f"NEAR CLI location: {which_result.stdout.strip()}")

            # First check if the account exists
            check_account = subprocess.run(
                ["near", "state", str(self.account)],
                capture_output=True,
                text=True,
                check=False
            )
            logger.info(f"Account state check result: {check_account.stdout}")

            if check_account.returncode != 0:
                logger.error(f"Account state check failed: {check_account.stderr}")
                raise ValueError(f"Failed to verify NEAR account state: {check_account.stderr}")

            # Generate key for the account
            generate_key = subprocess.run(
                ["near", "generate-key", str(self.account), "--networkId", "testnet"],
                capture_output=True,
                text=True,
                check=False
            )
            logger.info(f"Key generation result: {generate_key.stdout}")

            if generate_key.returncode != 0:
                logger.error(f"Key generation failed: {generate_key.stderr}")
                raise ValueError(f"Failed to generate key: {generate_key.stderr}")

            # Deploy the contract
            self._deploy_contract()

            logger.info("NEAR account setup successful")

        except Exception as e:
            logger.error(f"Error setting up NEAR account: {str(e)}")
            logger.exception("Full traceback:")
            raise

    def _deploy_contract(self):
        """Deploy the Rust prophecy contract to NEAR testnet"""
        try:
            logger.info("Building and deploying Rust prophecy contract...")

            # Build the contract
            build_result = subprocess.run(
                ["cargo", "build", "--target", "wasm32-unknown-unknown", "--release"],
                cwd="prophecy-contract",
                capture_output=True,
                text=True
            )

            if build_result.returncode != 0:
                logger.error(f"Failed to build Rust contract: {build_result.stderr}")
                raise ValueError("Failed to build Rust contract")

            logger.info("Contract built successfully")

            # Get the WASM file path
            wasm_path = "prophecy-contract/target/wasm32-unknown-unknown/release/prophecy_contract.wasm"

            if not os.path.exists(wasm_path):
                logger.error(f"WASM file not found at {wasm_path}")
                raise FileNotFoundError(f"Compiled WASM file not found")

            # Deploy the contract
            deploy_command = [
                "near",
                "deploy",
                "--accountId",
                self.account,
                "--wasmFile",
                wasm_path,
                "--initFunction",
                "new",
                "--initArgs",
                json.dumps({"owner_id": self.account})
            ]

            logger.info(f"Deploying contract with command: {' '.join(deploy_command)}")

            result = subprocess.run(
                deploy_command,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                logger.error(f"Contract deployment failed: {result.stderr}")
                raise ValueError(f"Failed to deploy contract: {result.stderr}")

            logger.info(f"Contract deployment successful: {result.stdout}")

        except Exception as e:
            logger.error(f"Error deploying contract: {str(e)}")
            logger.exception("Full traceback:")
            raise

    def _save_local(self, prophecy_id, prophecy_data):
        """Save prophecy to local storage"""
        try:
            with open(self.local_storage_path, 'r') as f:
                prophecies = json.load(f)
            prophecies[prophecy_id] = prophecy_data
            with open(self.local_storage_path, 'w') as f:
                json.dump(prophecies, f)
            return True
        except Exception as e:
            logger.error(f"Error saving to local storage: {str(e)}")
            return False

    def _get_local(self, prophecy_id):
        """Get prophecy from local storage"""
        try:
            with open(self.local_storage_path, 'r') as f:
                prophecies = json.load(f)
            return prophecies.get(prophecy_id)
        except Exception as e:
            logger.error(f"Error reading from local storage: {str(e)}")
            return None

    def store_prophecy(self, prophecy, timestamp):
        """Store a prophecy with fallback to local storage"""
        prophecy_id = f"prophecy_{timestamp}"

        # Try blockchain storage first if enabled
        if self.blockchain_enabled:
            try:
                command = [
                    "near",
                    "call",
                    self.account,
                    "store_prophecy",
                    json.dumps({
                        "prophecy_id": prophecy_id,
                        "text": prophecy
                    }),
                    "--accountId",
                    self.account
                ]

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    logger.info(f"Prophecy stored successfully on blockchain: {result.stdout}")
                    return True
                else:
                    logger.warning(f"Blockchain storage failed, falling back to local: {result.stderr}")
            except Exception as e:
                logger.warning(f"Error in blockchain storage, falling back to local: {str(e)}")

        # Fall back to local storage
        prophecy_data = {
            "text": prophecy,
            "timestamp": timestamp,
            "created_at": datetime.now().isoformat()
        }
        return self._save_local(prophecy_id, prophecy_data)

    def get_prophecy(self, timestamp):
        """Get a prophecy with fallback to local storage"""
        prophecy_id = f"prophecy_{timestamp}"

        # Try blockchain first if enabled
        if self.blockchain_enabled:
            try:
                command = [
                    "near",
                    "view",
                    self.account,
                    "get_prophecy",
                    json.dumps({
                        "prophecy_id": prophecy_id
                    })
                ]

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    return json.loads(result.stdout)
                else:
                    logger.warning(f"Blockchain retrieval failed, trying local storage: {result.stderr}")
            except Exception as e:
                logger.warning(f"Error in blockchain retrieval, trying local storage: {str(e)}")

        # Fall back to local storage
        return self._get_local(prophecy_id)