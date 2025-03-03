# Web3 Prophet Bot - NEAR Hackathon Submission

## Project Description
A Discord bot that generates mystical Web3 prophecies using OpenAI and stores them on the NEAR blockchain. This project is part of the "Absurd Agents" track, combining AI-generated content with blockchain persistence.

### Features
- AI-powered prophecy generation using GPT-4
- On-chain storage using NEAR Protocol
- Discord bot integration for easy access
- Local storage fallback for reliability

### Technical Stack
- Rust smart contract for NEAR blockchain
- Discord.py for bot functionality
- OpenAI API for prophecy generation
- Local JSON storage fallback

## Smart Contract Details
The smart contract provides:
- Secure prophecy storage with owner-only write access
- Efficient prophecy retrieval
- Timestamp-based prophecy tracking
- Query interface for latest prophecies

## Testing
Run tests using:
```bash
cargo test
```

## Deployment
Deploy to NEAR testnet using:
```bash
near deploy --accountId YOUR_ACCOUNT --wasmFile target/wasm32-unknown-unknown/release/prophecy_contract.wasm
```

## Hackathon Category: Absurd Agents
This project fits the "Absurd Agents" track by creating an AI-powered oracle that combines:
- Mystical prophecy generation
- Blockchain permanence
- Community interaction through Discord
