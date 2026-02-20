import sys
import os
import streamlit as st
import pandas as pd
import random
import time
import string
from datetime import datetime

# -------------------------------------------------
# Ensure project root on path
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.main import process_event


# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="TrustLens AI Demo",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 TrustLens AI – Live Demo")
st.caption("Real-time AI-powered cybersecurity monitoring for SMEs")


# -------------------------------------------------
# Sidebar Controls
# -------------------------------------------------
num_events = st.sidebar.slider("Events per refresh", 5, 50, 10)
refresh_rate = st.sidebar.slider("Refresh interval (seconds)", 1, 10, 5)


# -------------------------------------------------
# Known data pools (realistic)
# -------------------------------------------------
KNOWN_DEVICES = [
    "Dell Latitude 7420",
    "HP EliteBook 840",
    "Lenovo ThinkPad X1",
    "MacBook Pro 14”"
]

KNOWN_LOCATIONS = [
    "Nairobi, Kenya",
    "Mombasa, Kenya",
    "Kisumu, Kenya",
    "Kampala, Uganda"
]

ROLE_MAP = {
    1: "Employee",
    2: "Manager",
    3: "Administrator"
}

USERNAMES = [
    "alice.k", "bob.m", "charlie.t", "diana.s", "edward.l", "fiona.w"
]

UNKNOWN = "Unknown"


# -------------------------------------------------
# Helper functions
# -------------------------------------------------
def generate_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def generate_session():
    return "".join(random.choices(string.ascii_letters + string.digits, k=16))


def access_time(hour):
    now = datetime.now()
    return now.replace(hour=hour,
                       minute=random.randint(0, 59),
                       second=random.randint(0, 59)).strftime("%Y-%m-%d %H:%M:%S")


# -------------------------------------------------
# Event Types
# -------------------------------------------------
def normal_event():
    return {
        "login_hour": random.randint(8, 18),
        "device_known": 1,
        "location_known": 1,
        "access_count": random.randint(1, 5),
        "role_level": 1
    }


def medium_event():
    return {
        "login_hour": random.choice([6, 7, 19, 20]),
        "device_known": 1,
        "location_known": 1,
        "access_count": random.randint(6, 12),
        "role_level": random.choice([1, 2])
    }


def high_event():
    return {
        "login_hour": random.choice([0, 1, 2, 3, 22, 23]),
        "device_known": 1,
        "location_known": 1,
        "access_count": random.randint(15, 30),
        "role_level": 0
    }


# -------------------------------------------------
# Session state
# -------------------------------------------------
if "blocked_sessions" not in st.session_state:
    st.session_state.blocked_sessions = {}

if "cycle" not in st.session_state:
    st.session_state.cycle = 0


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
placeholder = st.empty()

while True:

    st.session_state.cycle += 1

    events = []

    high_prob = min(0.02 + st.session_state.cycle * 0.01, 0.3)

    for _ in range(num_events):
        r = random.random()
        if r < high_prob:
            events.append(high_event())
        elif r < 0.5:
            events.append(medium_event())
        else:
            events.append(normal_event())

    rows = []

    # -------------------------------------------------
    # Generate rows
    # -------------------------------------------------
    for e in events:

        result = process_event(e)

        is_employee = e["role_level"] in ROLE_MAP

        rows.append({
            "Access Time": access_time(e["login_hour"]),
            "Username": random.choice(USERNAMES) if is_employee else UNKNOWN,
            "IP Address": generate_ip(),
            "Session ID": generate_session(),
            "Device": random.choice(KNOWN_DEVICES),
            "Location": random.choice(KNOWN_LOCATIONS),
            "Role": ROLE_MAP.get(e["role_level"], UNKNOWN),
            "Access Count": e["access_count"],
            "Risk (%)": result["risk"],
            "Reasons": "; ".join(result["reasons"])
        })

    df = pd.DataFrame(rows)

    # -------------------------------------------------
    # UI
    # -------------------------------------------------
    with placeholder.container():

        st.subheader("📊 Live Event Risk Table")
        st.dataframe(df, use_container_width=True)

        # ---------------- Summary
        avg = round(df["Risk (%)"].mean(), 2)
        high = len(df[df["Risk (%)"] >= 70])
        med = len(df[(df["Risk (%)"] >= 40) & (df["Risk (%)"] < 70)])

        c1, c2, c3 = st.columns(3)
        c1.metric("Average Risk", f"{avg}%")
        c2.metric("High Risk", high)
        c3.metric("Medium Risk", med)

        # ---------------- High Risk Actions
        st.subheader("🔎 High-Risk Event Details")

        high_df = df[df["Risk (%)"] >= 70]

        if high_df.empty:
            st.success("✅ No active threats")
        else:
            for i, row in high_df.iterrows():

                sid = row["Session ID"]

                if sid not in st.session_state.blocked_sessions:
                    st.session_state.blocked_sessions[sid] = True

                blocked = st.session_state.blocked_sessions[sid]

                st.markdown(f"### 🚨 Event {i+1}")

                st.write(f"**Access Time:** {row['Access Time']}")
                st.write(f"**Username:** {row['Username']}")
                st.write(f"**IP:** {row['IP Address']}")
                st.write(f"**Session:** {sid}")
                st.write(f"**Risk Level:** {row['Risk (%)']}%")

                st.write("**Details:**")
                st.write(f"- Device: {row['Device']}")
                st.write(f"- Location: {row['Location']}")
                st.write(f"- Role: {row['Role']}")

                st.write("**Reasons:**")
                st.write(row["Reasons"])

                st.write("### ⚙️ System Actions Executed")

                st.warning("⚠️ Identity verification failed")
                st.info("🔄 Credentials automatically rotated")

                col1, col2 = st.columns(2)

                with col1:
                    st.button("🔴 BLOCKED", disabled=True, key=f"b{sid}")

                with col2:
                    if st.button("🟡 Unblock", key=f"u{sid}"):
                        st.session_state.blocked_sessions[sid] = False

                if not st.session_state.blocked_sessions[sid]:
                    st.success("🟢 Session manually unblocked")

                st.divider()

    time.sleep(refresh_rate)