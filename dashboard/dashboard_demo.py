import sys
import os
import streamlit as st
import pandas as pd
import random
import time
import string
from datetime import datetime, timedelta

# --- Ensure project root is on Python path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.main import process_event

# --- Page Config ---
st.set_page_config(
    page_title="TrustLens AI Demo",
    page_icon="🔐",
    layout="wide",
)

st.title("🔐 TrustLens AI – Live Demo")
st.caption("Real-time cybersecurity monitoring simulation for SMEs")

# --- Sidebar ---
num_events = st.sidebar.slider("Number of events per refresh", 5, 50, 10)
refresh_rate = st.sidebar.slider("Refresh interval (seconds)", 1, 10, 5)


# =========================
# Realistic Mappings
# =========================
KNOWN_DEVICES = [
    "Dell Latitude 7420",
    "HP EliteBook 840",
    "Lenovo ThinkPad X1",
    "MacBook Pro 14”",
]

KNOWN_LOCATIONS = [
    "Nairobi, Kenya",
    "Mombasa, Kenya",
    "Kisumu, Kenya",
    "Kampala, Uganda",
]

ROLE_MAP = {
    1: "Employee",
    2: "Manager",
    3: "Administrator",
}

UNKNOWN_LABEL = "Unknown"

USERNAMES = [
    "alice.k", "bob.m", "charlie.t", "diana.s", "edward.l", "fiona.w"
]


# =========================
# Resolvers
# =========================
def resolve_device(is_known):
    return random.choice(KNOWN_DEVICES) if is_known else UNKNOWN_LABEL


def resolve_location(is_known):
    return random.choice(KNOWN_LOCATIONS) if is_known else UNKNOWN_LABEL


def resolve_role(role_level, is_employee):
    if not is_employee:
        return UNKNOWN_LABEL
    return ROLE_MAP.get(role_level, UNKNOWN_LABEL)


def resolve_username(is_employee):
    return random.choice(USERNAMES) if is_employee else UNKNOWN_LABEL


def generate_access_time(login_hour):
    now = datetime.now()
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    access_time = now.replace(hour=login_hour, minute=minute, second=second)
    return access_time.strftime("%Y-%m-%d %H:%M:%S")


def generate_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def generate_session_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=16))


# =========================
# Event Generators
# =========================
def normal_event():
    return {
        "login_hour": random.randint(8, 18),
        "device_known": 1,
        "location_known": 1,
        "access_count": random.randint(1, 5),
        "role_level": 1
    }


def medium_risk_event():
    return {
        "login_hour": random.choice([6, 7, 19, 20]),
        "device_known": 1,
        "location_known": 1,
        "access_count": random.randint(6, 12),
        "role_level": random.choice([1, 2])
    }


def high_risk_event():
    # outsiders but device/location still visible
    return {
        "login_hour": random.choice([0, 1, 2, 3, 22, 23]),
        "device_known": 1,
        "location_known": 1,
        "access_count": random.randint(15, 30),
        "role_level": 0  # NOT a valid employee
    }


# --- Session state ---
if "cycle" not in st.session_state:
    st.session_state.cycle = 0

placeholder = st.empty()


# =========================
# Live Demo Loop
# =========================
while True:
    st.session_state.cycle += 1
    events = []

    high_risk_probability = min(0.02 + st.session_state.cycle * 0.01, 0.3)
    medium_risk_probability = 0.3

    for _ in range(num_events):
        roll = random.random()
        if roll < high_risk_probability:
            events.append(high_risk_event())
        elif roll < high_risk_probability + medium_risk_probability:
            events.append(medium_risk_event())
        else:
            events.append(normal_event())

    results = []

    for event in events:
        result = process_event(event)

        # 🔥 KEY FIX: determine if user is registered employee
        is_employee = event["role_level"] in ROLE_MAP

        results.append({
            "Access Time": generate_access_time(event["login_hour"]),
            "Username": resolve_username(is_employee),
            "IP Address": generate_ip(),
            "Session ID": generate_session_id(),
            "Device": resolve_device(event["device_known"]),
            "Location": resolve_location(event["location_known"]),
            "Access Count": event["access_count"],
            "Role": resolve_role(event["role_level"], is_employee),
            "Risk (%)": result["risk"],
            "Reasons": "; ".join(result["reasons"]),
        })

    df = pd.DataFrame(results)

    with placeholder.container():
        st.subheader("📊 Live Event Risk Table")
        st.dataframe(df, use_container_width=True)

        # --- Risk Summary ---
        avg_risk = round(df["Risk (%)"].mean(), 2)
        high_risk_count = len(df[df["Risk (%)"] >= 70])
        medium_risk_count = len(df[(df["Risk (%)"] >= 40) & (df["Risk (%)"] < 70)])

        st.subheader("📈 Risk Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Average Risk", f"{avg_risk}%")
        c2.metric("High-Risk Events", high_risk_count)
        c3.metric("Medium-Risk Events", medium_risk_count)

        if high_risk_count > 0:
            st.error("🚨 Active threats detected — immediate action required")
        elif avg_risk > 40:
            st.warning("⚠️ Suspicious behavior detected")
        else:
            st.success("✅ System operating normally")

        # --- High-Risk Details (kept exactly as you had) ---
        st.subheader("🔎 High-Risk Event Details")
        high_df = df[df["Risk (%)"] >= 70]

        if high_df.empty:
            st.info("No high-risk events detected in this interval.")
        else:
            for idx, row in high_df.iterrows():
                st.markdown(f"### 🚨 Event {idx + 1}")
                st.write(f"**Access Time:** {row['Access Time']}")
                st.write(f"**Username:** {row['Username']}")
                st.write(f"**IP Address:** {row['IP Address']}")
                st.write(f"**Session ID:** {row['Session ID']}")
                st.write(f"**Risk Level:** {row['Risk (%)']}%")
                st.write("**Details:**")
                st.write(f"- Device: {row['Device']}")
                st.write(f"- Location: {row['Location']}")
                st.write(f"- Role: {row['Role']}")
                st.write("**Reasons:**")
                st.write(row["Reasons"])
                st.write("**Recommended Action:**")
                st.write("• Verify user identity")
                st.write("• Block session if unverified")
                st.write("• Rotate credentials")
                st.divider()

    time.sleep(refresh_rate)
