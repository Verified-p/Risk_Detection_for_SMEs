from fastapi import FastAPI, Header, HTTPException, Request
from dotenv import load_dotenv
import os

from app.main import process_event

# Load .env variables
load_dotenv()

API_KEY = os.getenv("TRUSTLENS_API_KEY")

app = FastAPI(title="TrustLens AI API")


@app.get("/")
def health_check():
    return {"status": "TrustLens AI running"}


@app.post("/event")
async def receive_event(
    request: Request,
    x_api_key: str = Header(None)
):
    """
    Receives security events from bank-sme UI
    Verifies API key
    Sends to TrustLens AI engine
    Returns risk result
    """

    # 1️⃣ Validate API key exists
    if not API_KEY:
        raise HTTPException(status_code=500, detail="Server key not configured")

    # 2️⃣ Verify key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 3️⃣ Read event body safely
    event = await request.json()

    # 4️⃣ Process with AI engine
    result = process_event(event)

    # 5️⃣ Return response
    return result