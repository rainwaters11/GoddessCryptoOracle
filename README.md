# Web3 Prophet Oracle Bot

A Python-powered Web3 prophecy platform that generates mystical blockchain-integrated oracles through an innovative Discord bot and web interface, featuring refined and minimalist blockchain visualization.

## Features
- Discord bot for prophecy generation
- AI-powered prophecy generation using OpenAI
- NEAR blockchain integration for prophecy storage
- Web interface with 3D blockchain visualization
- Local storage fallback for reliability
- Minimal and elegant UI design

## Tech Stack
- Discord.py for bot functionality
- OpenAI API for prophecy generation
- NEAR Protocol for blockchain storage
- Flask web application
- Three.js for blockchain visualization
- Rust smart contracts

## Setup
1. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
DISCORD_TOKEN=your_discord_token
OPENAI_API_KEY=your_openai_key
NEAR_ACCOUNT=your_near_account
NEAR_PRIVATE_KEY=your_near_private_key
```

3. Run the application:
```bash
python web_app.py  # For web interface
python main.py     # For Discord bot
```

## Smart Contract
The NEAR smart contract is written in Rust and handles prophecy storage on the blockchain. Build and deploy:
```bash
cd prophecy-contract
cargo build --target wasm32-unknown-unknown --release
near deploy --accountId YOUR_ACCOUNT --wasmFile target/wasm32-unknown-unknown/release/prophecy_contract.wasm
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
ISC License
