from web3 import Web3
import json, hashlib, os
from dotenv import load_dotenv

load_dotenv()

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
contract_address = os.getenv('CONTRACT_ADDRESS')

# Load ABI (from Remix)
with open('IdentityManager.json') as f:
    abi = json.load(f)['abi']

contract = w3.eth.contract(address=contract_address, abi=abi)

# Hash data using SHA-256
def hash_data(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

# Register user identity on blockchain
def register_identity(email: str, govt_id: str, ipfs_cid: str):
    tx = contract.functions.setIdentity(
        hash_data(email),
        hash_data(govt_id),
        ipfs_cid
    ).buildTransaction({
        'chainId': 1337,
        'gas': 200000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'nonce': w3.eth.getTransactionCount(w3.eth.accounts[0])
    })
    signed_tx = w3.eth.account.signTransaction(tx, os.getenv('PRIVATE_KEY'))
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return tx_hash.hex()

# Verify user identity
def verify_identity(email: str, govt_id: str, user_address: str):
    stored_email_hash, stored_govt_hash, _ = contract.functions.getIdentity(user_address).call()
    current_email_hash = hash_data(email)
    current_govt_hash = hash_data(govt_id)
    return (current_email_hash == stored_email_hash) and (current_govt_hash == stored_govt_hash)