from sgp4.api import Satrec
from sgp4.api import jday
from datetime import datetime, timedelta
import math
import numpy as np

# Load Satellites Data TLE.

def load_satellite(name):

    try:
        with open("data/tle/satellites.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        satellites = []

        for i in range(0, len(lines), 5):
            satellites.append({
                "name": lines[i],
                "line1": lines[i+1],
                "line2": lines[i+2],
                "length": lines[i+3],
                "width": lines[i+4]
            })

        for sat in satellites:
            if sat['name'] == name:
                return sat
        print("Satellite not found!")

    except FileNotFoundError:
        print("TLE file not found")

# It loads all satellites

def load_all_satellites():

    with open("data/tle/satellites.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    satellites = []

    for i in range(0, len(lines), 5):

        satellites.append({
            "name": lines[i],
            "line1": lines[i+1],
            "line2": lines[i+2],
            "length": lines[i+3],
            "width": lines[i+4]
        })

    return satellites

# Propagate Satellites: It gives Error, Position, Velocity Values.

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

# Future Propagation: It find the Future Propagation of Satellites on the given Interval.

def future_propagation(line1, line2, interval, start_time=None):
    satellite = Satrec.twoline2rv(line1, line2)

    # BUG FIX: Agar bahar se start_time (jaise current_sim_time) aaya hai toh wo use karo, 
    # nahi toh default mein abhi ka utcnow() lo
    if start_time is None:
        now = datetime.utcnow()
    else:
        now = start_time

    results = []

    WINDOW_DAYS = 3

    # 1440 minutes = 24 ghante ki window chalegi loop mein
    for minute in range(0, WINDOW_DAYS * 24 * 60, interval):
        
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