import tracker
import conjunction
import maneuver
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

# TESTING RISK ENGINE

fake_miss_distance = 0.3  # km
fake_probability = 0.005

risk = conjunction.get_risk_level(
    fake_miss_distance,
    fake_probability
)

print("\n===== TEST RESULT =====")
print("Miss Distance:", fake_miss_distance)
print("Probability:", fake_probability)
print("Risk:", risk)
print("=======================")

# Test all risk levels
test_cases = [
    (0.3, 0.005, "CRITICAL expected"),
    (0.8, 0.00005, "HIGH expected"),
    (3.0, 0.000005, "MEDIUM expected"),
    (10.0, 0.0, "SAFE expected"),
]

for miss_d, prob, expected in test_cases:
    risk = conjunction.get_risk_level(miss_d, prob)
    print(f"{expected}: {risk}")

# Updated robust test suite
test_cases = [
    # Standard normal tests (Jo aapne kiye)
    (0.3, 0.005, "CRITICAL expected (Dono high)"),
    (0.8, 0.0002, "HIGH expected (Dono medium)"),
    (3.0, 0.00005, "MEDIUM expected (Dono low)"),
    (10.0, 0.0, "SAFE expected (Dono safe)"),
    
    # Advanced Edge Cases (Yahan asli logic check hoga)
    (8.0, 0.005, "CRITICAL expected (Distance door hai par PROBABILITY bohot high hai)"),
    (0.2, 0.0, "CRITICAL expected (Probability zero hai par DISTANCE bohot paas hai)")
]

print("\n===== RUNNING ROBUST RISK ASSESSMENT MATRIX =====")
for miss_d, prob, label in test_cases:
    risk = conjunction.get_risk_level(miss_d, prob)
    print(f"[{label}] -> Miss: {miss_d}km | Prob: {prob} -> Output: {risk}")
print("==================================================")
