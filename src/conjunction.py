import math
import numpy as np

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

    closest_time = None

    for point1, point2 in zip(traj1, traj2):
        distance = find_distance(point1["position"], point2["position"])

        if distance < minimum_distance:

            minimum_distance = distance

            closest_time = point1["time"]

    return minimum_distance, closest_time

# Dot Product: It finds the Dot Product of the two satellites that is usefull of analysing both satellites they are seperating or approaching

def dot_product(rel_pos, rel_vel):

    dot = np.dot(rel_pos, rel_vel)

    return dot