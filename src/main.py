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

    print(f"\n🚀 Loop Execute Hone Ka Current UTC Time: {datetime.utcnow()}")
    results = conjunction.full_conjunction_analysis(
        ISS,
        satellites
    )

    print(results[:10])
    print("-" * 50)

    time.sleep(600)

