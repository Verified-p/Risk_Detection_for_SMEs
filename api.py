from fastapi import FastAPI, Body
from app.main import process_event

app = FastAPI(
    title="TrustLens AI API",
    description="Real-time cybersecurity risk detection for SMEs",
    version="2.0"
)


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
# 🔥 Accept ANY SME JSON (no schema restriction)
@app.post("/analyze")
def analyze_event(event: dict = Body(...)):

    # pass raw event directly
    result = process_event(event)

    return {
        "risk": result["risk"],
        "reasons": result["reasons"],
        "verified": result["verified"],
        "blocked": result["blocked"],
        "credentials_rotated": result["credentials_rotated"],
        "recommended_action": (
            "Rotate credentials and verify user"
            if result["risk"] >= 70 else
            "Monitor activity closely"
            if result["risk"] >= 40 else
            "No action required"
        )
    }