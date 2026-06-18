from sgp4.api import Satrec
from sgp4.api import jday
from datetime import datetime
from tracker import *

sat = load_satellite("ISS (ZARYA)")

iss = Satrec.twoline2rv(sat["line1"], sat["line2"])

now = datetime.utcnow()

jd, fr = jday(
    now.year,
    now.month,
    now.day,
    now.hour,
    now.minute,
    now.second
)

e, r, v = iss.sgp4(jd, fr)

print("Error: ", e)
print("Position: ", r)
print("Velocity: ", v)