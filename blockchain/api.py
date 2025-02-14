from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from blockchain import register_identity, verify_identity
import os

app = FastAPI()

class UserRegistration(BaseModel):
    email: str
    govt_id: str
    ipfs_cid: str  # Mock encrypted document CID

class UserVerification(BaseModel):
    email: str
    govt_id: str
    user_address: str  # User's Ethereum address

@app.post("/register")
async def register(user: UserRegistration):
    # Use a test account private key (from Ganache)
    tx_hash = register_identity(
        user.email,
        user.govt_id,
        user.ipfs_cid,
        private_key=os.getenv('PRIVATE_KEY')
    )
    return {"tx_hash": tx_hash, "status": "Identity stored"}


@app.post("/verify")
async def verify(user: UserVerification):
    is_valid = verify_identity(user.email, user.govt_id, user.user_address)
    if is_valid:
        return {"status": "Verified"}
    else:
        raise HTTPException(status_code=401, detail="Authentication failed")
