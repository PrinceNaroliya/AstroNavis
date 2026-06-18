from sgp4.api import Satrec
from sgp4.api import jday
from datetime import datetime, timedelta
import math
import numpy as np

def load_satellite(name):

    try:
        with open("data/tle/satellites.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        satellites = []

        for i in range(0, len(lines), 3):
            satellites.append({
                "name": lines[i],
                "line1": lines[i+1],
                "line2": lines[i+2]
            })

        for sat in satellites:
            if sat['name'] == name:
                return sat
        print("Satellite not found!")

    except FileNotFoundError:
        print("TLE file not found")

def propagate_satellite(line1, line2):

    now = datetime.utcnow()

    satellite = Satrec.twoline2rv(line1, line2)

    jd, fr = jday(
        now.year,
        now.month,
        now.day,
        now.hour,
        now.minute,
        now.second
    )

    error, position, velocity = satellite.sgp4(jd, fr)

    return error, position, velocity

def find_distance(position1, position2):

    x1, y1, z1 = position1
    x2, y2, z2 = position2

    distance = math.sqrt(
        (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
    )

    return distance

def relative_position(position1, position2):

    x1, y1, z1 = position1
    x2, y2, z2 = position2

    return (
        x2 - x1,
        y2 - y1,
        z2 - z1
    )

def relative_velocity(velocity1, velocity2):

    x1, y1, z1 = velocity1
    x2, y2, z2 = velocity2

    return (
        x2 - x1,
        y2 - y1,
        z2 - z1
    )

def relative_speed(velocity1, velocity2):

    x1, y1, z1 = velocity1
    x2, y2, z2 = velocity2

    return math.sqrt(
        (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2
    )

def future_propagation(line1, line2, interval):

    satellite = Satrec.twoline2rv(line1, line2)

    now = datetime.utcnow()

    results = []

    for minute in range(0, 1440, interval):
        
        future_time = now + timedelta(minutes=minute)

        jd, fr = jday(
            future_time.year,
            future_time.month,
            future_time.day,
            future_time.hour,
            future_time.minute,
            future_time.second
        )

        e, r, v = satellite.sgp4(jd, fr)

        results.append(
            {
                "time": future_time,
                "error": e,
                "position": r,
                "velocity": v
            }
        )

    return results

def closest_approach(traj1, traj2):

    minimum_distance = float("inf")

    closest_time = None

    for point1, point2 in zip(traj1, traj2):
        distance = find_distance(point1["position"], point2["position"])

        if distance < minimum_distance:

            minimum_distance = distance

            closest_time = point1["time"]

    return minimum_distance, closest_time

def dot_product(rel_pos, rel_vel):

    dot = np.dot(rel_pos, rel_vel)

    return dot