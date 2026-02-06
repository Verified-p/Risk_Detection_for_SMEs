from fastapi import FastAPI
from pydantic import BaseModel
from app.main import process_event

app = FastAPI(
    title="TrustLens AI API",
    description="Real-time cybersecurity risk detection for SMEs",
    version="1.0"
)

# =========================
# DATA MODEL
# =========================
class SecurityEvent(BaseModel):
    login_hour: int
    device_known: int
    location_known: int
    access_count: int
    role_level: int

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def health_check():
    return {
        "status": "active",
        "message": "TrustLens AI is protecting your system"
    }

# =========================
# REAL-TIME RISK ANALYSIS
# =========================
@app.post("/analyze")
def analyze_event(event: SecurityEvent):
    result = process_event(event.dict())

    return {
        "risk": result["risk"],
        "reasons": result["reasons"],
        "recommended_action": (
            "Rotate credentials and verify user"
            if result["risk"] > 70 else
            "Monitor activity closely"
            if result["risk"] > 40 else
            "No action required"
        )
    }
