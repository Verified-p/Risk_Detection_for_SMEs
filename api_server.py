from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
import os

from app.main import process_event

load_dotenv()
API_KEY = os.getenv("TRUSTLENS_API_KEY")

app = FastAPI()


@app.post("/event")
def receive_event(event: dict, x_api_key: str = Header(None)):

    # 1️⃣ Verify API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid key")

    # 2️⃣ Process the event
    result = process_event(event)  # returns a dict with risk, blocked, rotated, verified, reasons

    # 3️⃣ Return the processed result
    return result