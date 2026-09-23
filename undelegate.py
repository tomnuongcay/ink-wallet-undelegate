import sys
from web3 import Web3
from eth_account import Account

# ==============================================================================
# 1. NETWORK & RPC CONFIGURATION
# ==============================================================================
# Replace with your network RPC URL (e.g., Alchemy, QuickNode, or Public RPC)
RPC_URL = "https://ink-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("❌ Error: Unable to connect to RPC endpoint. Please check your network or API key.")
    sys.exit(1)

print("✅ Connected to network successfully!")

# ==============================================================================
# 2. PRIVATE KEYS & ACCOUNTS
# ==============================================================================
# ⚠️ WARNING: Keep your private keys secure. Never commit keys to public repositories.
HACKED_PRIVATE_KEY = "YOUR_COMPROMISED_WALLET_PRIVATE_KEY"
SPONSOR_PRIVATE_KEY = "YOUR_SPONSOR_WALLET_PRIVATE_KEY"

hacked_account = Account.from_key(HACKED_PRIVATE_KEY)
sponsor_account = Account.from_key(SPONSOR_PRIVATE_KEY)

print(f"📍 Compromised Wallet (Target) : {hacked_account.address}")
print(f"📍 Sponsor Wallet (Gas Payer)  : {sponsor_account.address}")

# 0x00...00 represents the null address to clear/undelegate EIP-7702 authorization
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

# ==============================================================================
# 3. EIP-7702 AUTHORIZATION SIGNING (OFFLINE)
# ==============================================================================
chain_id = w3.eth.chain_id
nonce_hacked = w3.eth.get_transaction_count(hacked_account.address)

auth_tuple = {
    'chainId': chain_id,
    'address': ZERO_ADDRESS,  # Resets delegation back to a standard EOA
    'nonce': nonce_hacked
}

# Sign the authorization tuple using the compromised wallet's key
signed_auth = Account.sign_authorization(auth_tuple, HACKED_PRIVATE_KEY)
print("🔑 EIP-7702 Authorization signed successfully!")

# ==============================================================================
# 4. TYPE-4 TRANSACTION CONSTRUCTIONS (SPONSORED GAS)
# ==============================================================================
sponsor_nonce = w3.eth.get_transaction_count(sponsor_account.address)

# Dynamic fee estimation
base_fee = w3.eth.get_block('latest')['baseFeePerGas']
max_priority_fee = w3.to_wei('0.05', 'gwei')
max_fee = base_fee * 2 + max_priority_fee

tx_eip7702 = {
    'type': 4,  # EIP-7702 Type-4 Transaction
    'chainId': chain_id,
    'nonce': sponsor_nonce,
    'to': hacked_account.address,
    'value': 0,
    'gas': 150000,
    'maxFeePerGas': max_fee,
    'maxPriorityFeePerGas': max_priority_fee,
    'authorizationList': [signed_auth]
}

# Sponsor wallet signs and broadcasts the transaction
signed_tx = w3.eth.account.sign_transaction(tx_eip7702, SPONSOR_PRIVATE_KEY)

print("🚀 Broadcasting EIP-7702 undelegation transaction...")

# Compatible with different web3.py/eth-account versions
tx_raw = getattr(signed_tx, 'raw_transaction', getattr(signed_tx, 'rawTransaction', None))
tx_hash = w3.eth.send_raw_transaction(tx_raw)

print(f"🔗 Transaction Hash: {tx_hash.hex()}")

# ==============================================================================
# 5. EXECUTION CONFIRMATION
# ==============================================================================
print("⏳ Waiting for block confirmation...")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

if receipt['status'] == 1:
    print("\n🎉 SUCCESS: EIP-7702 delegation removed! The account has reverted to a standard EOA.")
else:
    print("\n❌ FAILURE: Transaction reverted. Check gas limits or account nonces.")
