import random
import json

osm_ids = [
    "48036846",
    "48041477",
    "48056837",
    "55333016",
    "67110575",
    "67596879",
    "121777219",
    "295818812",
    "295820309",
    "295846649",
    "295846650",
    "296252750",
    "296507400",
    "297401965",
    "297527532",
    "331160766",
    "655490174",
    "732099139",
    "893122330",
    "306011118",
    "306011599",
    "306020851",
    "306496893",
    "306499334",
    "306507109",
    "306512939",
    "306514470",
    "306515312",
    "306516802",
    "307055376",
    "307072199",
    "307076753",
    "307120468",
    "367141870",
    "804064065",
    "4076119232",
    "8097533191",
    "8097555034",
]


def simulate():
    file = open("simulation_5.json", "w")
    time = 24
    capacity_per_hour = []
    for _ in range(1, time + 1):
        unavailable_fire_stations = []
        availability_dict = {}
        for osm in osm_ids:
            capacity = random.randint(0, 5)
            if capacity == 0:
                unavailable_fire_stations.append(osm)
            availability_dict[osm] = capacity
        capacity_per_hour.append(
            {
                "capacity": availability_dict,
                "unavailable_fire_stations": unavailable_fire_stations,
            }
        )
    json.dump(capacity_per_hour, file)


simulate()
