import streamlit as st
from streamlit_autorefresh import st_autorefresh

from skyfield.api import EarthSatellite, load
from datetime import datetime
import math

import tracker
import conjunction

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="AstroNavis",
    page_icon="🚀",
    layout="wide"
)

st_autorefresh(
    interval=60000,
    key="dashboard_refresh"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_resource
def load_satellites():

    iss = tracker.load_satellite("ISS (ZARYA)")
    satellites = tracker.load_all_satellites()

    return iss, satellites


ISS, satellites = load_satellites()

# ==========================================================
# CALCULATE LIVE DATA
# ==========================================================

def calculate_dashboard():

    # Current State
    error, position, velocity = tracker.propagate_satellite(
        ISS["line1"],
        ISS["line2"]
    )

    px, py, pz = position
    vx, vy, vz = velocity

    speed = math.sqrt(
        vx**2 +
        vy**2 +
        vz**2
    )

    # Skyfield
    ts = load.timescale()

    sat = EarthSatellite(
        ISS["line1"],
        ISS["line2"]
    )

    geo = sat.at(ts.now())

    subpoint = geo.subpoint()

    latitude = subpoint.latitude.degrees
    longitude = subpoint.longitude.degrees
    altitude = subpoint.elevation.km

    # Conjunction
    results = conjunction.full_conjunction_analysis(
        ISS,
        satellites
    )

    if len(results) == 0:

        return None

    closest = results[0]

    # NORAD
    norad = ISS["line1"].split()[1][:5]

    return {

        "error": error,

        "position": position,

        "velocity": velocity,

        "px": px,
        "py": py,
        "pz": pz,

        "vx": vx,
        "vy": vy,
        "vz": vz,

        "speed": speed,

        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,

        "results": results,

        "closest": closest,

        "norad": norad

    }


data = calculate_dashboard()

if data is None:

    st.error("No Threats Found")

    st.stop()

TEST_MODE = True

if TEST_MODE:

    data["closest"]["risk"] = "🔴 HIGH RISK"
    data["closest"]["name"] = "COSMOS 1234"
    data["closest"]["miss_distance"] = 0.82
    data["closest"]["time_to_tca"] = "18 min"
    data["closest"]["probability"] = 0.00235

# ==========================================================
# HEADER
# ==========================================================

st.title("🚀 AstroNavis Orbital Intelligence Platform")

st.caption(
    "Real-Time Orbital Conjunction Monitoring System"
)

st.divider()

# ==========================================================
# FIRST ROW
# ==========================================================

left, right = st.columns(2)

# ==========================================================
# SATELLITE INFORMATION
# ==========================================================

with left:

    st.subheader("🛰 Satellite Information")

    c1, c2 = st.columns(2)

    c1.metric(
        "Satellite",
        ISS["name"]
    )

    c2.metric(
        "NORAD ID",
        data["norad"]
    )

    c1.metric(
        "Altitude",
        f"{data['altitude']:.2f} km"
    )

    c2.metric(
        "Speed",
        f"{data['speed']:.2f} km/s"
    )

    c1.metric(
        "Latitude",
        f"{data['latitude']:.2f}°"
    )

    c2.metric(
        "Longitude",
        f"{data['longitude']:.2f}°"
    )

    c1.metric(
        "Propagation Error",
        data["error"]
    )

    c2.metric(
        "Last Update",
        datetime.utcnow().strftime("%H:%M:%S UTC")
    )

# ==========================================================
# THREAT SUMMARY
# ==========================================================

with right:

    threat = data["closest"]

    st.subheader("⚠ Threat Summary")

    c1, c2 = st.columns(2)

    c1.metric(
        "Closest Object",
        threat["name"]
    )

    c2.metric(
        "Miss Distance",
        f"{threat['miss_distance']:.2f} km"
    )

    c1.metric(
        "Time To TCA",
        threat["time_to_tca"]
    )

    c2.metric(
        "Collision Risk",
        threat["risk"]
    )

    c1.metric(
        "Probability",
        f"{threat['probability']:.2e}"
    )

st.divider()

# ==========================================================
# POSITION & VELOCITY
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("📍 Current Position (ECI)")

    st.metric(
        "X",
        f"{data['px']:.2f} km"
    )

    st.metric(
        "Y",
        f"{data['py']:.2f} km"
    )

    st.metric(
        "Z",
        f"{data['pz']:.2f} km"
    )

with right:

    st.subheader("🚀 Current Velocity (ECI)")

    st.metric(
        "VX",
        f"{data['vx']:.4f} km/s"
    )

    st.metric(
        "VY",
        f"{data['vy']:.4f} km/s"
    )

    st.metric(
        "VZ",
        f"{data['vz']:.4f} km/s"
    )

st.divider()

# ==========================================================
# THREAT COUNTS
# ==========================================================

threat_500 = 0
threat_100 = 0
threat_50 = 0

for obj in data["results"]:

    if obj["miss_distance"] < 500:
        threat_500 += 1

    if obj["miss_distance"] < 100:
        threat_100 += 1

    if obj["miss_distance"] < 50:
        threat_50 += 1

c1, c2, c3 = st.columns(3)

c1.metric(
    "Threats < 500 km",
    threat_500
)

c2.metric(
    "Threats < 100 km",
    threat_100
)

c3.metric(
    "Threats < 50 km",
    threat_50
)

st.divider()

# ==========================================================
# LIVE THREAT TABLE
# ==========================================================

st.subheader("🛰 Live Conjunction Monitor")

table = []

for obj in data["results"][:10]:

    table.append({

        "Satellite":
            obj["name"],

        "Miss Distance (km)":
            round(obj["miss_distance"],2),

        "Time To TCA":
            obj["time_to_tca"],

        "Probability":
            f'{obj["probability"]:.2e}',

        "Risk":
            obj["risk"]

    })

st.table(table)

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🚀 AstroNavis")

    st.success("System Online")

    st.markdown("---")

    st.subheader("Current Satellite")

    st.write(ISS["name"])

    st.write(f"NORAD : {data['norad']}")

    st.markdown("---")

    st.subheader("Prediction")

    st.write("Window : 72 Hours")

    st.write("Interval : 1 Minute")

    st.write(f"Objects : {len(satellites)}")

    st.markdown("---")

    st.subheader("Refresh")

    st.write(datetime.utcnow().strftime("%d-%m-%Y"))

    st.write(datetime.utcnow().strftime("%H:%M:%S UTC"))

st.divider()

# ==========================================================
# CLOSEST OBJECT
# ==========================================================

st.subheader("🛰 Closest Object")

closest = data["closest"]

# Relative Speed
rv = closest["rv_tca"]

relative_speed = math.sqrt(
    rv[0]**2 +
    rv[1]**2 +
    rv[2]**2
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Object Name",
        closest["name"]
    )

    st.metric(
        "Miss Distance",
        f"{closest['miss_distance']:.2f} km"
    )

    st.metric(
        "Time To TCA",
        closest["time_to_tca"]
    )

    st.metric(
        "TCA",
        closest["tca"].strftime("%d %b %Y %H:%M UTC")
    )

with col2:

    st.metric(
        "Relative Speed",
        f"{relative_speed:.2f} km/s"
    )

    st.metric(
        "Approaching",
        "YES" if closest["motion"] == "🔴 APPROACHING" else "NO"
    )

    st.metric(
        "Dot Product",
        f"{closest['dot_product']:.2f}"
    )

    st.metric(
        "Risk Level",
        closest["risk"]
    )

st.divider()

# ==========================================================
# SYSTEM HEALTH
# ==========================================================

st.subheader("🖥️ System Health")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Loaded Satellites",
        len(satellites)
    )

    st.metric(
        "Propagation Window",
        "72 Hours"
    )

    st.metric(
        "Propagation Interval",
        "1 Minute"
    )

    st.metric(
        "Engine Status",
        "🟢 ONLINE"
    )

with col2:

    st.metric(
        "Risk Engine",
        "🟢 ONLINE"
    )

    st.metric(
        "Conjunction Engine",
        "🟢 ONLINE"
    )

    st.metric(
        "Dashboard Refresh",
        "60 Seconds"
    )

    st.metric(
        "Prediction Status",
        "🟢 ACTIVE"
    )

st.divider()

# ==========================================================
# ALERTS
# ==========================================================

st.subheader("🚨 Alerts")

highest_risk = None

# Sabse pehla High/Critical object dhundo
for obj in data["results"]:

    if obj["risk"] != "🟢 SAFE":
        highest_risk = obj
        break


# ==========================================================
# NO ALERT
# ==========================================================

if highest_risk is None:

    st.success("✅ No Active Alerts")


# ==========================================================
# ACTIVE ALERT
# ==========================================================

else:

    st.error("⚠️ HIGH RISK OBJECT DETECTED")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Object",
            highest_risk["name"]
        )

        st.metric(
            "Distance",
            f"{highest_risk['miss_distance']:.2f} km"
        )

    with col2:

        st.metric(
            "Time To TCA",
            highest_risk["time_to_tca"]
        )

        st.metric(
            "Risk Level",
            highest_risk["risk"]
        )

st.divider()

# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    "AstroNavis © Orbital Intelligence Platform"
)