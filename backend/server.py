import sys
import signal
import time

sys.path.append("C:\\Users\\HP\\miniconda3\\lib\\site-packages")

from flask import Flask, request, make_response
import json
from main import calcShortestPath, getRandomPoints

app = Flask(__name__)


@app.route("/getShortestPath", methods=["POST"])
def shortestPath():
    global simulation_data
    data = dict(request.form)["latlng"]
    lng = json.loads(data)["lng"]
    lat = json.loads(data)["lat"]

    timePeriod = int(dict(request.form)["timePeriod"])
    unavailable_fire_stations = simulation_data[timePeriod]["unavailable_fire_stations"]

    calcShortestPath(lng, lat, unavailable_fire_stations.copy())
    actual_path = ""
    with open("path.json", "r") as f:
        actual_path = json.dumps(json.load(f))

    calcShortestPath(lng, lat, [])
    optimal_path = ""
    with open("path.json", "r") as f:
        optimal_path = json.dumps(json.load(f))

    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.data = json.dumps(
        {"success": True, "actual_path": actual_path, "optimal_path": optimal_path}
    )
    return response


@app.route("/", methods=["GET"])
def home():
    return "Server up and running"


if __name__ == "__main__":
    with open("simulation.json") as f:
        simulation_data = json.load(f)
    app.run(port=5000)
