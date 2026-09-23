# ink-wallet-undelegate
A lightweight Python tool to revoke and undelegate malicious EIP-7702 authorizations on Ink Chain using sponsored gas.
# 🦑 Ink Chain EIP-7702 Rescue Tool

A simple Python script to remove/undelegate malicious EIP-7702 contract authorizations on Ink Chain using sponsored gas.

## 🚀 Quick Start

### Install Dependencies

python3 -m venv venv
source venv/bin/activate

pip install --upgrade web3 eth-account

### Configuration

Open `undelegate.py` and replace the placeholder values:
- `RPC_URL`: Your Ink Chain RPC (e.g., Alchemy/QuickNode)
- `HACKED_PRIVATE_KEY`: Private key of the compromised account
- `SPONSOR_PRIVATE_KEY`: Private key of the clean account paying gas

### Execute

python undelegate.py

## 🛡️ Disclaimer

For educational and emergency recovery purposes only. Use at your own risk. Never commit private keys to GitHub.
