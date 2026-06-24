from skyfield.api import EarthSatellite, load
import tracker
import conjunction
import math
from datetime import datetime

ISS = tracker.load_satellite("ISS (ZARYA)")
satellites = tracker.load_all_satellites()

ts = load.timescale()

sat = EarthSatellite(ISS["line1"], ISS["line2"])

t = ts.now()

geocentric = sat.at(t)

subpoint = geocentric.subpoint()

latitude = subpoint.latitude.degrees
longitude = subpoint.longitude.degrees
altitude = subpoint.elevation.km

e, r, v = tracker.propagate_satellite(ISS["line1"], ISS["line2"])

x1, y1, z1 = r
x2, y2, z2 = v

velocity = (x2, y2, z2)

def calculate_speed(velocity):

    vx, vy, vz = velocity

    speed = math.sqrt(
        vx**2 +
        vy**2 +
        vz**2
    )

    return speed

sat_speed = calculate_speed(velocity)

def get_norad_id(line1):

    parts = line1.split()

    return parts[1][0:5]

narod_id = get_norad_id(ISS["line1"])

results = conjunction.full_conjunction_analysis(
    ISS,
    satellites
)

risk = results[0]["risk"]

last_update = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

print("_"*40)
print("\n🚀 ASTRONAVIS ORBITAL INTELLIGENCE PLATFORM")
print("SATELLITE                              THREAT SUMMARY")
print("_"*40)
print("\nName: ISS(ZARYA)                       ","Closest Object: ", results[0]["name"])
print(f"\nNAROD ID: {narod_id}                  Miss Distance: {results[0]["miss_distance"]} ")
print(f"\nRisk:  {risk}                         Time to TCA: {results[0]["time_to_tca"]}")
print(f"\nSpeed: {sat_speed:.2f} km/s           Collision Risk: {risk}")
print(f"\nERROR:  {e}                           Probability: {results[0]["probability"]}")
print("_" * 40)
print(f"\nPosition X:  {x1}                     CLOSEST OBJECT")
print(f"\nPosition Y:  {y1}                     TCA: {results[0]["tca"]}")
print(f"\nPosition Z:  {z1}                     Relative Speed {rel_speed}")
print("_" * 40)
print(f"\nVelocity X:  {x2}")
print(f"\nVelocity Y:  {y2}")
print(f"\nVelocity Z:  {z2}")
print("_" * 40)
print(f"\nLatitude:  {latitude}")
print(f"\nLongitude:  {longitude}")
print(f"\nAltitude:  {altitude}")
print("_" * 40)
print(f"\nLast Update:  {last_update}")
