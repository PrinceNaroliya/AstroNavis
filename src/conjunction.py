import math
import numpy as np
import tracker
from datetime import datetime

# Find Distance: It finds Distance between Two Satellites.

def find_distance(position1, position2):

    x1, y1, z1 = position1
    x2, y2, z2 = position2

    distance = math.sqrt(
        (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
    )

    return distance

# Relative Position: It finds Relative Position between two Satellites.

def relative_position(position1, position2):

    x1, y1, z1 = position1
    x2, y2, z2 = position2

    return (
        x2 - x1,
        y2 - y1,
        z2 - z1
    )

# Relative Velocity: It finds Relative Velocity between two Satellites.

def relative_velocity(velocity1, velocity2):

    x1, y1, z1 = velocity1
    x2, y2, z2 = velocity2

    return (
        x2 - x1,
        y2 - y1,
        z2 - z1
    )

# Relative Speed: It finds Relative Speed between two Satellites.

def relative_speed(velocity1, velocity2):

    x1, y1, z1 = velocity1
    x2, y2, z2 = velocity2

    return math.sqrt(
        (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
    )

# Closest Approach: It find the Closest Approach between two Satellites.

def closest_approach(traj1, traj2):

    minimum_distance = float("inf")

    position1_at_tca = None
    position2_at_tca = None

    velocity1_at_tca = None
    velocity2_at_tca = None

    closest_time = None

    for point1, point2 in zip(traj1, traj2):
        distance = find_distance(point1["position"], point2["position"])

        if distance < minimum_distance:

            minimum_distance = distance

            closest_time = point1["time"]

            position1_at_tca = point1["position"]

            position2_at_tca = point2["position"]

            velocity1_at_tca = point1["velocity"]

            velocity2_at_tca = point2["velocity"]

    return (
        minimum_distance,
        closest_time,
        position1_at_tca,
        position2_at_tca,
        velocity1_at_tca,
        velocity2_at_tca
        )

# Dot Product: It finds the Dot Product of the two satellites that is usefull of analysing both satellites they are seperating or approaching

def dot_product(rel_pos, rel_vel):

    dot = np.dot(rel_pos, rel_vel)

    return dot

def calculate_hbr(sat1, sat2):

    diagnol1 = math.sqrt(float(sat1["length"])**2 + float(sat1["width"])**2)
    radius1 = math.ceil(diagnol1/2)

    diagnol2 = math.sqrt(float(sat2["length"])**2 + float(sat2["width"])**2)
    radius2 = math.ceil(diagnol2/2)

    hbr_meters = radius1 + radius2

    hbr_km = hbr_meters/1000.0

    return hbr_km

def build_encounter_frame(rr_tca, rv_tca):

    z_b = rv_tca / np.linalg.norm(rv_tca)

    cross_prod1 = np.cross(rr_tca, z_b)
    x_b = cross_prod1 / np.linalg.norm(cross_prod1)

    y_b = np.cross(z_b, x_b)

    return x_b, y_b, z_b

import numpy as np

def project_to_b_plane(rr_tca, covariance, x_b, y_b, z_b):

    M = np.vstack([x_b, y_b, z_b])

    r_b = M @ np.array(rr_tca)
    x_m = r_b[0] # 2D plane ka X coordinate
    y_m = r_b[1] # 2D plane ka Y coordinate

    cov_b = M @ np.array(covariance) @ M.T
 
    covariance_2d = cov_b[0:2, 0:2]

    return x_m, y_m, covariance_2d

def find_probability(rr_tca, rv_tca, hbr, covariance=None):
    # Khel yahan hai: Agar main code se covariance nahi aayi, tabhi test waali matrix banegi
    if covariance is None:
        sigma = 0.1  # 0.1 km = 100 meters uncertainty
        covariance1 = np.eye(3) * (sigma**2)  # np.eye(3) se direct diagonal matrix ban jati hai
        covariance2 = np.eye(3) * (sigma**2)
        covariance = covariance1 + covariance2
    else:
        covariance = np.array(covariance)

    # 1. Pehle 3D axes banaye
    x_b, y_b, z_b = build_encounter_frame(rr_tca, rv_tca)
    
    # 2. 3D data ko 2D B-Plane par project kiya
    x_m, y_m, covariance_2d = project_to_b_plane(rr_tca, covariance, x_b, y_b, z_b)
    
    # 3. 2D Covariance ko diagonalize (seedha) kiya
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_2d)
    
    # Sigmas (Standard Deviations) nikale
    sigma_x = math.sqrt(max(1e-10, eigenvalues[0]))
    sigma_y = math.sqrt(max(1e-10, eigenvalues[1]))
    
    # 4. Position vector ko naye frame me rotate kiya
    rotated_pos = eigenvectors.T @ np.array([x_m, y_m])
    x_p = rotated_pos[0]
    y_p = rotated_pos[1]
    
    # 5. Foster's Probability Formula Calculation
    exponent = -0.5 * ((x_p**2 / sigma_x**2) + (y_p**2 / sigma_y**2))
    
    # Math overflow check
    if exponent < -700:
        return 0.0
        
    coefficient = (hbr**2) / (2.0 * sigma_x * sigma_y)
    probability = math.exp(exponent) * coefficient
 
    return min(1.0, probability)

def find_risky_objects(user_satellite, all_satellites, start_time=None):

    results = []

    if start_time is None:
        start_time = datetime.utcnow()

    user_traj = tracker.future_propagation(
        user_satellite["line1"],
        user_satellite["line2"],
        1,
        start_time=start_time
    )

    for sat in all_satellites:

        if sat["name"] == user_satellite["name"]:
            continue

        other_traj = tracker.future_propagation(
            sat["line1"],
            sat["line2"],
            1,
            start_time=start_time
        )

        (
            miss_distance,
            tca,
            pos1_tca,
            pos2_tca,
            vel1_tca,
            vel2_tca
        ) = closest_approach(
            user_traj,
            other_traj
        )

        rr_tca = relative_position(
            pos1_tca,
            pos2_tca
        )

        rv_tca = relative_velocity(
            vel1_tca,
            vel2_tca
        )

        dot = dot_product(
            rr_tca,
            rv_tca
        )

        hbr = calculate_hbr(
            user_satellite,
            sat
        )

        if dot < 0:
            motion_status = "🔴 APPROACHING"

        elif dot > 0:
            motion_status = "🟢 SEPARATING"

        else:
            motion_status = "🟡 CROSSING"

        results.append({

            "name": sat["name"],

            "miss_distance": miss_distance,

            "tca": tca,

            "rr_tca": rr_tca,

            "rv_tca": rv_tca,

            "dot_product": dot,

            "motion_status": motion_status,

            "hbr": hbr

        })

    results.sort(
        key=lambda x: x["miss_distance"]
    )

    return results

def get_risk_level(miss_distance, pc):

    if miss_distance < 0.5 or pc > 0.001:
        return "☠️ CRITICAL"

    elif miss_distance < 1 or pc > 0.0001:
        return "🔴 HIGH RISK"

    elif miss_distance < 5 or pc > 0.00001:
        return "🟠 MEDIUM RISK"

    else:
        return "🟢 SAFE"

def full_conjunction_analysis(user_satellite, all_satellites, current_sim_time=None):

    if current_sim_time is None:
        current_sim_time = datetime.utcnow()

    risky_objects = find_risky_objects(
        user_satellite,
        all_satellites,
        start_time=current_sim_time
    )

    results = []

    for obj in risky_objects:
        if obj["miss_distance"] > 500:
            break  # Sorted hai, baaki sab aur door

        tca_dt = obj["tca"]
        if tca_dt.tzinfo is not None:
            tca_dt = tca_dt.replace(tzinfo=None)

        time_to_tca = tca_dt - current_sim_time
        total_seconds = time_to_tca.total_seconds()

        if total_seconds <= 0:
            # Event past mein nikal chuka hai, active thread matrix se hatao!
            continue 

        # BUG FIX 2: Safe Positive Time Delta Formatting (No weird modulo behavior)
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        pc = find_probability(obj["rr_tca"], obj["rv_tca"], obj["hbr"])
        risk = get_risk_level(obj["miss_distance"], pc)

        results.append({
            "name": obj["name"],
            "miss_distance": obj["miss_distance"],
            "tca": obj["tca"],
            "time_to_tca": f"{hours}h {minutes}m",
            "probability": pc,
            "dot_product": obj["dot_product"],
            "motion": obj["motion_status"],
            "risk": risk
        })

    return results

