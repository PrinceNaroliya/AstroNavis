import tracker
import conjunction
import maneuver
import numpy as np
import math

# Load Sattelites

ISS = tracker.load_satellite("ISS (ZARYA)")

HUBBLE = tracker.load_satellite("HUBBLE SPACE TELESCOPE")

iss_line1 = ISS["line1"]
iss_line2 = ISS["line2"]

hubble_line1 = HUBBLE["line1"]
hubble_line2 = HUBBLE["line2"]

# Propagate Satellites

e1, r1, v1 = tracker.propagate_satellite(iss_line1, iss_line2)
e2, r2, v2 = tracker.propagate_satellite(hubble_line1, hubble_line2)

# Relative Position

rel_position = conjunction.relative_position(r1, r2)

# Relative Velocity

rel_velocity = conjunction.relative_velocity(v1, v2)

# Relative Speed

rel_speed = conjunction.relative_speed(v1, v2)

# Distance

distance = conjunction.find_distance(r1, r2)

# Future Propagation

iss_fut_propagation = tracker.future_propagation(iss_line1, iss_line2, 10)

hubble_fut_propagation = tracker.future_propagation(hubble_line1, hubble_line2, 10)

# Minimum Distance or Time of Closest Approach

(miss_distance,tca,pos1_tca,pos2_tca,vel1_tca,vel2_tca) = conjunction.closest_approach(iss_fut_propagation, hubble_fut_propagation)

# Dot Product

dot_prod = conjunction.dot_product(rel_position, rel_velocity)
print("Dot Product between two Satellites: ", dot_prod)

if dot_prod < 0:
    print("⚠️ Approaching!")
else:
    print("✅ Separating")

r_hat, t_hat, n_hat = maneuver.rtn_frame(iss_line1, iss_line2)

'''
print(r_hat, t_hat, n_hat)

print(np.linalg.norm(r_hat))
print(np.linalg.norm(t_hat))
print(np.linalg.norm(n_hat))

print(np.dot(r_hat, t_hat))

print(np.dot(r_hat, n_hat))

print(np.dot(t_hat, n_hat))
'''

'''
import numpy as np
import plotly.graph_objects as go

# ==========================================
# SATELLITE POSITIONS
# ==========================================

pos_iss = np.array([-2225, 3753, 5193])
pos_hubble = np.array([3000, 4000, 2000])

# ==========================================
# EARTH
# ==========================================

earth_radius = 6371

theta = np.linspace(0, 2*np.pi, 80)
phi = np.linspace(0, np.pi, 80)

theta, phi = np.meshgrid(theta, phi)

earth_x = earth_radius * np.cos(theta) * np.sin(phi)
earth_y = earth_radius * np.sin(theta) * np.sin(phi)
earth_z = earth_radius * np.cos(phi)

# ==========================================
# BUBBLE FUNCTION
# ==========================================

def create_sphere(center, radius):

    u = np.linspace(0, 2*np.pi, 50)
    v = np.linspace(0, np.pi, 50)

    u, v = np.meshgrid(u, v)

    x = center[0] + radius * np.cos(u) * np.sin(v)
    y = center[1] + radius * np.sin(u) * np.sin(v)
    z = center[2] + radius * np.cos(v)

    return x, y, z

# ==========================================
# COLLISION BUBBLES
# ==========================================

bubble_radius = 1000

iss_x, iss_y, iss_z = create_sphere(
    pos_iss,
    bubble_radius
)

hub_x, hub_y, hub_z = create_sphere(
    pos_hubble,
    bubble_radius
)

# ==========================================
# FIGURE
# ==========================================

fig = go.Figure()

# ==========================================
# EARTH
# ==========================================

fig.add_trace(
    go.Surface(
        x=earth_x,
        y=earth_y,
        z=earth_z,
        opacity=0.85,
        showscale=False,
        name="Earth"
    )
)

# ==========================================
# ISS BUBBLE
# ==========================================

fig.add_trace(
    go.Surface(
        x=iss_x,
        y=iss_y,
        z=iss_z,
        opacity=0.25,
        colorscale=[[0, "yellow"], [1, "yellow"]],
        showscale=False,
        name="ISS Collision Zone"
    )
)

# ==========================================
# HUBBLE BUBBLE
# ==========================================

fig.add_trace(
    go.Surface(
        x=hub_x,
        y=hub_y,
        z=hub_z,
        opacity=0.25,
        colorscale=[[0, "cyan"], [1, "cyan"]],
        showscale=False,
        name="Hubble Collision Zone"
    )
)

# ==========================================
# SATELLITE POINTS
# ==========================================

fig.add_trace(
    go.Scatter3d(
        x=[pos_iss[0]],
        y=[pos_iss[1]],
        z=[pos_iss[2]],
        mode="markers",
        marker=dict(
            size=8,
            color="yellow"
        ),
        name="ISS"
    )
)

fig.add_trace(
    go.Scatter3d(
        x=[pos_hubble[0]],
        y=[pos_hubble[1]],
        z=[pos_hubble[2]],
        mode="markers",
        marker=dict(
            size=8,
            color="cyan"
        ),
        name="Hubble"
    )
)

# ==========================================
# LINE BETWEEN SATELLITES
# ==========================================

fig.add_trace(
    go.Scatter3d(
        x=[pos_iss[0], pos_hubble[0]],
        y=[pos_iss[1], pos_hubble[1]],
        z=[pos_iss[2], pos_hubble[2]],
        mode="lines",
        line=dict(
            width=4
        ),
        name="Relative Distance"
    )
)

# ==========================================
# LAYOUT
# ==========================================

fig.update_layout(
    title="AstroNavis Collision Bubble Demo",
    scene=dict(
        xaxis_title="X (km)",
        yaxis_title="Y (km)",
        zaxis_title="Z (km)",
        aspectmode="data",
        bgcolor="black"
    ),
    paper_bgcolor="black",
    font=dict(color="white")
)

fig.show()
'''

report = {
    'current_distance': distance,
    'relative_speed': rel_speed,
    'tca': tca,
    'miss_distance': miss_distance
}

rr_tca = conjunction.relative_position(
    pos1_tca,
    pos2_tca
)

rv_tca = conjunction.relative_velocity(
    vel1_tca,
    vel2_tca
)

hbr = conjunction.calculate_hbr(ISS, HUBBLE)

# --- TESTING FOSTER PROBABILITY ENGINE ---

# 1. Hamare paas HBR pehle se ready hai (0.073 km)
print(f"Using HBR: {hbr} km")

# 4. Function call karo (abhi covariance pass nahi kar rahe, toh default 100m uncertainty chalegi)
p_collision = conjunction.find_probability(rr_tca, rv_tca, hbr)

# 5. Output print karo ekdum clean format mein
print("---------------------------------------")
print(f"Calculated Collision Probability: {p_collision}")
print(f"Scientific Notation: {p_collision:.6e}")
print("---------------------------------------")

satellites = tracker.load_all_satellites()

results = conjunction.find_risky_objects(
    ISS,
    satellites
)

print(results[:10])