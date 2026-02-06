import streamlit as st
import sys
import os
import pandas as pd
import json
import sqlite3
import time
import ast
import random
import string
from datetime import datetime

# --- Ensure project root is on Python path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.main import process_event
from app.config import DB_PATH

# --- Page Config ---
st.set_page_config(
    page_title="TrustLens AI",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 TrustLens AI")
st.caption("AI-powered cybersecurity risk detection for SMEs")

# =========================
# CONSTANTS & HELPERS
# =========================
ROLE_MAP = {
    1: "Employee",
    2: "Manager",
    3: "System Administrator"
}

KNOWN_DEVICES = [
    "Dell Latitude 5420",
    "HP ProBook 450",
    "MacBook Pro 14”",
    "Lenovo ThinkPad X1",
]

LOCATIONS = [
    "Nairobi, Kenya",
    "Kisumu, Kenya",
    "Mombasa, Kenya",
    "Outside Kenya",
]

USERNAMES = [
    "alice.k", "bob.m", "charlie.t", "diana.s", "edward.l"
]

UNKNOWN = "Unknown"


def generate_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def generate_session_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=16))


def save_event_to_db(event, risk):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO audit (event, risk) VALUES (?, ?)",
        (json.dumps(event), risk)  # ✅ always valid JSON
    )
    conn.commit()
    conn.close()


def safe_parse_event(raw_event):
    try:
        return json.loads(raw_event)
    except Exception:
        try:
            return ast.literal_eval(raw_event)
        except Exception:
            return {}


# =========================
# SECTION 1: Analyze Single Event
# =========================
st.subheader("🔍 Analyze Single Security Event")

device_known = st.checkbox("Known device")
location_known = st.checkbox("Known location")
role_level = st.selectbox("Role level", [1, 2, 3])

event = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "username": random.choice(USERNAMES),
    "ip_address": generate_ip(),
    "session_id": generate_session_id(),
    "login_hour": st.slider("Login hour", 0, 23, 10),
    "device_known": int(device_known),
    "device_name": st.selectbox(
        "Device",
        KNOWN_DEVICES if device_known else [UNKNOWN]
    ),
    "location_known": int(location_known),
    "location_name": st.selectbox(
        "Location",
        LOCATIONS if location_known else [UNKNOWN]
    ),
    "access_count": st.number_input("Access count", 0, 50, 5),
    "role_level": role_level,
    "role_name": ROLE_MAP.get(role_level, UNKNOWN)
}

if st.button("Analyze Event", use_container_width=True):
    result = process_event(event)
    save_event_to_db(event, result["risk"])

    st.divider()
    st.metric("Risk Level", f"{result['risk']}%")

    st.subheader("Why this risk?")
    for reason in result["reasons"]:
        st.write("•", reason)

    if result["risk"] >= 70:
        st.error("🚨 Immediate action required")
    elif result["risk"] >= 40:
        st.warning("⚠️ Monitor activity closely")
    else:
        st.success("✅ Activity appears safe")

# =========================
# SECTION 2: Live Event Operations
# =========================
st.divider()
st.subheader("⏱️ Live Event Operations")

if st.button("View Live Events"):
    placeholder = st.empty()

    while True:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(
            "SELECT rowid AS id, event, risk FROM audit ORDER BY rowid DESC LIMIT 50",
            conn
        )
        conn.close()

        if df.empty:
            placeholder.info("No live events detected yet.")
        else:
            rows = []
            for _, r in df.iterrows():
                event = safe_parse_event(r["event"])

                rows.append({
                    "Time": event.get("timestamp"),
                    "Username": event.get("username"),
                    "IP Address": event.get("ip_address"),
                    "Session ID": event.get("session_id"),
                    "Device": event.get("device_name", UNKNOWN),
                    "Location": event.get("location_name", UNKNOWN),
                    "Role": event.get("role_name", UNKNOWN),
                    "Access Count": event.get("access_count"),
                    "Risk (%)": r["risk"]
                })

            placeholder.dataframe(pd.DataFrame(rows), use_container_width=True)

        time.sleep(3)

# =========================
# SECTION 3: Risk Trend
# =========================
st.divider()
st.subheader("📈 Risk Trend Over Time")

conn = sqlite3.connect(DB_PATH)
df_trend = pd.read_sql("SELECT rowid AS id, risk FROM audit ORDER BY rowid ASC", conn)
conn.close()

if not df_trend.empty:
    df_trend["seq"] = range(1, len(df_trend) + 1)
    st.line_chart(df_trend.set_index("seq")["risk"])
    st.success("✅ Risk trend loaded successfully")
else:
    st.info("No audit data available yet.")
