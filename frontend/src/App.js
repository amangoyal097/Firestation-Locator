import { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, useMap, useMapEvent } from 'react-leaflet'
import { GeoJSON } from "react-leaflet";
import L from "leaflet";
import fire_stations from "./map_data/fire_stations.json";
import washington from "./map_data/washington.json"
import "./App.css";
import fire_truck from "./markers/fire_truck.js";
import axios from "axios";
import Loading from "./components/Loading";
import Alert from "./components/Alert";
import Snackbar from "@mui/material/Snackbar";
import Grid from "@mui/material/Grid";
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';

const mapBounds = [[38.79164435125649, -77.11979521874902], [38.995968036511364, -76.90914995593276]]


const App = () => {

  const [selecting, setSelecting] = useState(false);
  const [mapZoom, setMapZoom] = useState(null);
  const [mapCenter, setMapCenter] = useState(null)
  const [userMarker, setUserMarker] = useState();
  const [currPath, setCurrPath] = useState({ "actual_path": null, "optimal_path": null });
  const [loading, setLoading] = useState(false);
  const [hourIndex, setHourIndex] = useState(0);

  const RenderBoundary = () => {
    const map = useMap();
    const fire_stations_layer = new L.geoJson(fire_stations, {
      pointToLayer: (feature, latlng) =>
        L.marker(latlng, { icon: fire_truck, title: "" })
    });
    var nexrad = L.tileLayer.wms("http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi", {
      layers: 'nexrad-n0r-900913',
      format: 'image/png',
      transparent: true,
      attribution: "Weather data © 2012 IEM Nexrad"
    });
    map.addLayer(fire_stations_layer);
    map.setMinZoom(12)
    return <GeoJSON key="boundary" data={washington} />
  }

  const MapClick = () => {
    const map = useMapEvent('click', (e) => {
      if (selecting) {
        setSelecting(false);
        if (userMarker)
          map.removeLayer(userMarker);
        if (currPath["actual_path"])
          map.removeLayer(currPath["actual_path"].layer);
        if (currPath["optimal_path"])
          map.removeLayer(currPath["optimal_path"].layer)

        setCurrPath({ "actual_path": null, "optimal_path": null });

        const formData = new FormData();
        formData.set("latlng", JSON.stringify(e.latlng));
        formData.set("timePeriod", hourIndex)

        const tempMarker = L.marker(e.latlng);
        setUserMarker(tempMarker);
        map.addLayer(tempMarker);
        setLoading(true);


        var config = {
          method: 'post',
          url: 'http://localhost:5000/getShortestPath',
          headers: {},
          data: formData
        };

        axios(config)
          .then(function (response) {
            const actual_path = {
              layer: new L.geoJson(JSON.parse(response.data.actual_path), {
                style: {
                  color: "red",
                  weight: 5,
                }
              }), time: JSON.parse(response.data.actual_path).features[0].properties.shortest_distance * 60
            };
            const optimal_path = {
              layer: new L.geoJson(JSON.parse(response.data.optimal_path), {
                style: {
                  color: "green",
                  weight: 5,
                }
              }), time: JSON.parse(response.data.optimal_path).features[0].properties.shortest_distance * 60
            };
            setCurrPath({ "actual_path": actual_path, "optimal_path": optimal_path });
            map.addLayer(actual_path.layer);
            map.addLayer(optimal_path.layer);
            setLoading(false);

          })
          .catch(function (error) {
            console.log(error);
            setLoading(false);
          });
      }

    });
    return null
  }

  const handleSnackClose = (_, reason) => {
    if (reason === "clickaway") {
      return;
    }
    setSelecting(false);
  };

  const Legend = () => {
    return <Grid container p={2} justifyContent="space-between" alignItems="center" className="legend">
      <Grid item xs={5}>
        <div className="optimal"></div>
      </Grid>
      <Grid item xs={6} className="time">{currPath.optimal_path.time.toFixed(1)} minutes</Grid>
      <Grid item xs={5}>
        <div className="actual"></div>
      </Grid>
      <Grid item xs={6} className="time">{currPath.actual_path.time.toFixed(1)} minutes</Grid>
    </Grid>
  }

  const getHour = (index) => {
    const time = new Date(2022, 10, 10, index);
    return time.toLocaleString('en-US', { hour: 'numeric', hour12: true })
  }

  const TimeSelect = () => {
    return <div className="time-select">
      <Select
        labelId="hour-select"
        id="demo-simple-select"
        value={hourIndex}
        className="select-hour"
        onChange={(e) => setHourIndex(e.target.value)}
        sx={{
          fontFamily: "Montserrat", width: "200px", textAlign: "center", fontWeight: "bold"
        }}
        MenuProps={{
          style: {
            maxHeight: 400,
          },
        }}
      >
        {
          Array(24).fill().map((_, i) => i).map((value) => <MenuItem sx={{
            fontFamily: "Montserrat", textAlign: "center", fontWeight: "bold"
          }} className="hour-text" value={value} key={value}>{getHour(value) + "-" + getHour(value + 1)}</MenuItem>)
        }
      </Select>
    </div>
  }

  return (
    <>
      {loading && <Loading />}
      <TimeSelect />
      {currPath.optimal_path !== null && <Legend />}
      <Snackbar
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
        open={selecting}
        onClose={handleSnackClose}
      >
        <Alert
          onClose={handleSnackClose}
          severity="info"
          sx={{ width: "100%", fontFamily: "Montserrat" }}
        >
          Click within the boundary to select point
        </Alert>
      </Snackbar>
      <MapContainer bounds={mapBounds} style={{ height: "100vh", background: "white" }} scrollWheelZoom={true} touchZoom={false} doubleClickZoom={false} >
        <div className="select-point" onClick={() => {
          setSelecting(true)
        }}>Select Point</div>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          opacity={0.4}
        />
        <MapClick />
        <RenderBoundary />
      </MapContainer>
    </>
  );
}

export default App;
