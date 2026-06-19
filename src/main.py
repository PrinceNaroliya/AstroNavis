import tracker
import conjunction

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

print("Postion of the ISS Satellite: ", r1)
print("Position of the HUBBLE Satellite: ", r2)

print("Velocity of the ISS Satellite: ", v1)
print("Velocity of the HUBBLE Satellite: ", v2)

# Relative Position

rel_position = conjunction.relative_position(r1, r2)
print("Relative Position between ISS and HUBBLE: ", rel_position)

# Relative Velocity

rel_velocity = conjunction.relative_velocity(v1, v2)
print("Relative Velocity between ISS and HUBBLE: ", rel_velocity)

# Relative Speed

rel_speed = conjunction.relative_speed(v1, v2)
print("Relative Speed between ISS and HUBBLE: ", rel_speed)

# Distance

distance = conjunction.find_distance(r1, r2)
print("Distance between ISS and HUBBLE: ", distance)

# Future Propagation

iss_fut_propagation = tracker.future_propagation(iss_line1, iss_line2, 10)
print("Future Propagation of the ISS: ", len(iss_fut_propagation))

hubble_fut_propagation = tracker.future_propagation(hubble_line1, hubble_line2, 10)
print("Future Propagation of the HUBBLE: ", len(hubble_fut_propagation))

# Minimum Distance or Time of Closest Approach

min_dist, tca = conjunction.closest_approach(iss_fut_propagation, hubble_fut_propagation)
print("Minimum Distance between ISS and HUBBLE: ", min_dist)
print("Time of Closest Approach between ISS and HUBBLE: ", tca)

# Dot Product

dot_prod = conjunction.dot_product(rel_position, rel_velocity)
print("Dot Product between ISS and HUBBLE: ", dot_prod)

if dot_prod < 0:
    print("⚠️ Approaching!")
else:
    print("✅ Separating")