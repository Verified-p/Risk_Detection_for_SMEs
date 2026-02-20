import streamlit as st
import pandas as pd
import sqlite3
import json
import ast
import sys
import os
import time

# PATH FIX
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.config import DB_PATH

UNKNOWN = "Unknown"

# PAGE CONFIG
st.set_page_config(
    page_title="TrustLens AI – Production Monitor",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 TrustLens AI – Production Monitor")
st.caption("AI-powered real-time cybersecurity protection for SMEs")

# HELPERS
def safe_parse_event(raw):
    try:
        return json.loads(raw)
    except:
        try:
            return ast.literal_eval(raw)
        except:
            return {}

def load_data():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql(
            "SELECT rowid AS id, * FROM audit ORDER BY rowid DESC LIMIT 50",
            conn
        )
    except:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

# AUTO REFRESH
refresh = st.sidebar.slider("Refresh interval (seconds)", 1, 10, 3)
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
if time.time() - st.session_state.last_refresh > refresh:
    st.session_state.last_refresh = time.time()
    st.rerun()

# LOAD EVENTS
df = load_data()
if df.empty:
    st.info("No events received yet from SME systems.")
    st.stop()

# TABLE VIEW
rows = []
for _, r in df.iterrows():
    e = safe_parse_event(r.get("event", "{}"))

    reasons_text = r.get("reasons") or "Normal login activity detected"

    rows.append({
        "RowID": r["id"],
        "Time": r.get("timestamp", UNKNOWN),
        "User": e.get("username", UNKNOWN),
        "IP": e.get("ip_address", UNKNOWN),
        "Session": e.get("session_id", UNKNOWN),
        "Device": e.get("device_name", "Windows Laptop"),
        "Location": e.get("location_name", "Kisumu Office"),
        "Role": e.get("role_name", UNKNOWN),
        "Risk (%)": int(r.get("risk", 0)),
        "Reasons": reasons_text,
        "Verified": "✅" if r.get("verified", 0) else "❌",
        "Blocked": "🔴 Yes" if r.get("blocked", 0) else "🟢 No",
        "Rotated": "🔄 Yes" if r.get("credentials_rotated", 0) else "No"
    })

display_df = pd.DataFrame(rows)
st.dataframe(display_df.drop(columns=["RowID"]), width="stretch")
# =================================================
# ADMIN CONTROL
# =================================================
st.subheader("Admin Controls – Manual Release Only")

blocked_rows = display_df[display_df["Blocked"] == "🔴 Yes"]

if blocked_rows.empty:
    st.success("No active blocks. System is secure.")
else:
    # Iterate safely using itertuples()
    for row in blocked_rows.itertuples(index=False):
        rid = row.RowID          # guaranteed scalar
        sid = row.Session
        if st.button(f"🟡 Unblock session: {sid}", key=f"unblock_{rid}"):
            conn = sqlite3.connect(DB_PATH)
            conn.execute("UPDATE audit SET blocked=0 WHERE rowid=?", (rid,))
            conn.commit()
            conn.close()
            st.success(f"Session {sid} released")
            st.rerun()

# RISK TREND
st.divider()
st.subheader("📈 Risk Trend")
st.line_chart(df["risk"])

# REASONS DISPLAY
st.subheader("🔍 Risk Reasons for Last 50 Events")
for _, r in display_df.iterrows():
    st.markdown(
        f"**{r['Time']} – User: {r['User']} – Risk: {r['Risk (%)']}%**  \n"
        f"Reasons: {r['Reasons']}"
    )