from sgp4.api import Satrec

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