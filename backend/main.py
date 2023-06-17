import sys

sys.path.append("C:\\OSGeo4W\\apps\\qgis\\python")
sys.path.append("C:\\OSGeo4W\\apps\\qgis\\python\\plugins")

from qgis.core import *

QgsApplication.setPrefixPath("C:\\Program Files\\QGIS2\\apps\\qgis", True)
app = QgsApplication([], True)
QgsApplication.initQgis()

from processing.core.Processing import Processing

Processing.initialize()
import processing

fire_stations = "D:\\Assignments\\Spatial\\Project\\fire_stations.shp"
road_network = "D:\\Assignments\\Spatial\\Project\\Roadway_Block.shp"
coordinates = "-77.03175246332975,38.91317581929987 [EPSG:4326]"


def calcShortestPath(lng, lat, unavailable_fire_stations):
    print("Getting available fire stations")

    vector_layer = QgsVectorLayer(fire_stations)

    available_fire_stations = processing.run(
        "qgis:executesql",
        {
            "INPUT_DATASOURCES": vector_layer,
            "INPUT_GEOMETRY_CRS": None,
            "INPUT_GEOMETRY_FIELD": "",
            "INPUT_GEOMETRY_TYPE": 2,
            "INPUT_QUERY": "select * from input1 where osm_id NOT IN "
            + "("
            + ",".join(["'{}'".format(value) for value in unavailable_fire_stations])
            + ")",
            "INPUT_UID_FIELD": "",
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )["OUTPUT"]

    print(available_fire_stations.featureCount())

    print("Executing Distance Matrix")
    config = {
        "DEFAULT_DIRECTION": 2,
        "DEFAULT_SPEED": 50,
        "DIRECTION_FIELD": "SUMMARYDIR",
        "END_POINTS": available_fire_stations,
        "INPUT": "D:/Assignments/Spatial/final/road_network.shp",
        "OUTPUT": "TEMPORARY_OUTPUT",
        "START_POINT": "%f,%f" % (lng, lat),
        "STRATEGY": 1,
        "TOLERANCE": 1.5e-05,
        "VALUE_BACKWARD": "IB",
        "VALUE_BOTH": "BD",
        "VALUE_FORWARD": "OB",
    }

    distance_matrix = processing.run("native:shortestpathpointtolayer", config)[
        "OUTPUT"
    ]

    print("Executing SQL")

    closest_feature = processing.run(
        "qgis:executesql",
        {
            "INPUT_DATASOURCES": distance_matrix,
            "INPUT_GEOMETRY_CRS": None,
            "INPUT_GEOMETRY_FIELD": "",
            "INPUT_GEOMETRY_TYPE": 3,
            "INPUT_QUERY": "select osm_id, min(cost) as shortest_distance, geometry\nfrom input1",
            "INPUT_UID_FIELD": "",
            "OUTPUT": "TEMPORARY_OUTPUT",
        },
    )["OUTPUT"]

    print("Processing finisehd")

    QgsVectorFileWriter.writeAsVectorFormat(
        closest_feature,
        "D:\\Assignments\\Spatial\\final\\backend\\path.json",
        "utf-8",
        QgsCoordinateReferenceSystem("EPSG:4326"),
        "GeoJson",
    )
    print("File written")


def getRandomPoints(count):
    random_points = processing.run(
        "native:randompointsinpolygons",
        {
            "INCLUDE_POLYGON_ATTRIBUTES": True,
            "INPUT": "D:/Assignments/Spatial/final/spatial-project/src/map_data/washington.json|layername=Washington_DC_Boundary",
            "MAX_TRIES_PER_POINT": 10,
            "MIN_DISTANCE": 0,
            "MIN_DISTANCE_GLOBAL": 0,
            "OUTPUT": "TEMPORARY_OUTPUT",
            "POINTS_NUMBER": count,
            "SEED": None,
        },
    )["OUTPUT"]
    points = []
    for feature in random_points.getFeatures():
        x = feature.geometry().asPoint().x()
        y = feature.geometry().asPoint().y()
        points.append([x, y])
    return points
