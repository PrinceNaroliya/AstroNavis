import tracker
import conjunction
import maneuver
import visualization
import numpy as np
import math
from datetime import datetime
import time

# Load Sattelites

ISS = tracker.load_satellite("ISS (ZARYA)")

satellites = tracker.load_all_satellites()

while True:

    results = conjunction.full_conjunction_analysis(
        ISS,
        satellites
    )

    print(results[:10])

    time.sleep(600)

