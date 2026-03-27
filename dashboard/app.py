import streamlit as st
import pandas as pd
import sqlite3
import json
import ast
import sys
import os
import time
import pydeck as pdk

# PATH FIX
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.config import DB_PATH

UNKNOWN = "Unknown"

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="TrustLens AI – System Monitor",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 TrustLens AI – System Monitor")
st.caption("AI-powered real-time cybersecurity protection for SMEs")

# ==========================
# HELPERS
# ==========================
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
            "SELECT rowid AS id, * FROM audit ORDER BY rowid DESC LIMIT 100",
            conn
        )
    except:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

def safe_float(val):
    try:
        return float(val)
    except:
        return None

# ==========================
# AUTO REFRESH
# ==========================
refresh = st.sidebar.slider("Refresh interval (seconds)", 1, 10, 3)

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > refresh:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()

# ==========================
# LOAD EVENTS
# ==========================
df = load_data()

if df.empty:
    st.info("No events received yet from SME systems.")
    st.stop()

# ==========================
# BUILD TABLE
# ==========================
rows = []
map_points = []

for _, r in df.iterrows():

    e = safe_parse_event(r.get("event", "{}"))

    username = e.get("user") or UNKNOWN
    ip_address = e.get("ip") or UNKNOWN
    device_name = e.get("device") or UNKNOWN
    location_name = e.get("location") or UNKNOWN
    role_name = e.get("role") or UNKNOWN
    session_id = e.get("session_id") or UNKNOWN

    lat = safe_float(e.get("lat"))
    lon = safe_float(e.get("lon"))

    risk_value = int(r.get("risk", 0))
    reasons_text = r.get("reasons") or "Normal login activity detected"

    if lat is not None and lon is not None:
        map_points.append({
            "lat": lat,
            "lon": lon,
            "risk": risk_value
        })

    rows.append({
        "RowID": r["id"],
        "Time": r.get("timestamp", UNKNOWN),
        "User": username,
        "IP": ip_address,
        "Session": session_id,
        "Device": device_name,
        "Location": location_name,
        "Role": role_name,
        "Risk (%)": risk_value,
        "Reasons": reasons_text,
        "Verified": "✅" if r.get("verified", 0) else "❌",
        "Blocked": "🔴 Yes" if r.get("blocked", 0) else "🟢 No",
        "Rotated": "🔄 Yes" if r.get("credentials_rotated", 0) else "No"
    })

display_df = pd.DataFrame(rows)

# ==========================
# DISPLAY TABLE
# ==========================
st.subheader("🔎 Security Events")

st.dataframe(
    display_df.drop(columns=["RowID"]),
    use_container_width=True
)

# ==========================
# ADMIN CONTROL
# ==========================
st.subheader("🛠 Admin Controls – Manual Release")

blocked_rows = display_df[display_df["Blocked"] == "🔴 Yes"]

if blocked_rows.empty:
    st.success("No active blocks. System secure.")
else:

    for row in blocked_rows.itertuples(index=False):

        rid = row.RowID
        sid = row.Session

        if st.button(f"🟡 Unblock session {sid}", key=f"unblock_{rid}"):

            conn = sqlite3.connect(DB_PATH)
            conn.execute(
                "UPDATE audit SET blocked=0 WHERE rowid=?",
                (rid,)
            )
            conn.commit()
            conn.close()

            st.success(f"Session {sid} released")
            st.experimental_rerun()

# ==========================
# RISK TREND
# ==========================
st.divider()
st.subheader("📈 Risk Trend")

st.line_chart(df["risk"])

# ==========================
# GLOBAL CYBER HEATMAP
# ==========================
st.divider()
st.subheader("🌍 Global Cyber Activity")

if map_points:

    map_df = pd.DataFrame(map_points)

    if len(map_df) >= 3:
        # Heatmap for many events
        layer = pdk.Layer(
            "HeatmapLayer",
            data=map_df,
            get_position='[lon, lat]',
            get_weight='risk',
            radiusPixels=60,
        )
    else:
        # Scatter fallback for few points
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position='[lon, lat]',
            get_radius=30000,
            get_fill_color='[255, 0, 0, 160]',
            pickable=True,
        )

    view_state = pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom=1
    )

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/dark-v9"
        )
    )

else:
    st.warning("No geolocation events detected yet. Login again from the SME system.")

# ==========================
# RISK REASONS
# ==========================
st.divider()
st.subheader("🧠 Risk Explanations")

for _, r in display_df.iterrows():

    st.markdown(
        f"**{r['Time']} – User: {r['User']} – Risk: {r['Risk (%)']}%**  \n"
        f"Reasons: {r['Reasons']}"
    )