import json
from main import calcShortestPath


def getData():
    with open("random_points.json", "r") as f:
        points = json.load(f)
    optimal_times = []
    cnt = 1
    for feature in points["features"]:
        print("Optimal Path for Point %d" % (cnt))
        cnt += 1
        calcShortestPath(*feature["geometry"]["coordinates"], [])
        with open("path.json", "r") as f:
            optimal_times.append(
                json.load(f)["features"][0]["properties"]["shortest_distance"] * 60
            )

    with open("simulation_5.json", "r") as f:
        simulation_data = json.load(f)
    actual_times = []
    cnt = 1
    for feature in points["features"]:
        actual_times_point = []
        hourtime = 1
        for hour in simulation_data:
            print("Actual Path for Point %d on Hour %d " % (cnt, hourtime))
            hourtime += 1
            calcShortestPath(
                *feature["geometry"]["coordinates"],
                hour["unavailable_fire_stations"].copy()
            )
            with open("path.json", "r") as f:
                actual_times_point.append(
                    json.load(f)["features"][0]["properties"]["shortest_distance"] * 60
                )
        actual_times.append(actual_times_point)
        cnt += 1

    data = {}
    data["optimal_times"] = optimal_times
    data["actual_times"] = actual_times

    with open("data_5.json", "w") as f:
        json.dump(data, f)


getData()
