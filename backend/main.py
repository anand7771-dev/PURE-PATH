from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# 🔑 API KEYS
ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImUyMDEwNjBkZDRiMTRjZDJiYzA1Njg3OTVjMTQ3NmU1IiwiaCI6Im11cm11cjY0In0="
WAQI_API_KEY = "5fa3adc92909f3e6befc9dea717eb98a1922f490"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteRequest(BaseModel):
    source: str
    destination: str


@app.get("/")
def root():
    return {"status": "PurePath backend running"}


# ---------- GEOCODING (ORS) ----------
def geocode(place: str):
    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": ORS_API_KEY,
        "text": place,
        "size": 1
    }

    res = requests.get(url, params=params).json()

    if "features" not in res or len(res["features"]) == 0:
        return None

    return res["features"][0]["geometry"]["coordinates"]  # [lon, lat]


# ---------- AQI (WAQI) ----------
def get_aqi(lat, lon):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/"
    params = {"token": WAQI_API_KEY}

    res = requests.get(url, params=params).json()

    if res["status"] != "ok":
        return None

    return res["data"]["aqi"]


def aqi_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


# ---------- ROUTE + AQI ----------
@app.post("/routes")
def get_route(data: RouteRequest):

    src = geocode(data.source)
    dst = geocode(data.destination)

    if not src or not dst:
        return {"error": "Invalid location name"}

    # OSRM ROUTING
    osrm_url = (
        f"http://router.project-osrm.org/route/v1/driving/"
        f"{src[0]},{src[1]};{dst[0]},{dst[1]}"
        f"?overview=full&geometries=geojson"
    )

    route_res = requests.get(osrm_url).json()

    if "routes" not in route_res or len(route_res["routes"]) == 0:
        return {"error": "Route not found"}

    route = route_res["routes"][0]

    # AQI FETCH
    src_aqi = get_aqi(src[1], src[0])
    dst_aqi = get_aqi(dst[1], dst[0])

    return {
        "distance_km": round(route["distance"] / 1000, 2),
        "time_min": round(route["duration"] / 60, 2),
        "geometry": route["geometry"]["coordinates"],

        "source": [src[1], src[0]],
        "destination": [dst[1], dst[0]],

        "source_aqi": src_aqi,
        "destination_aqi": dst_aqi,
        "source_aqi_status": aqi_category(src_aqi) if src_aqi else "N/A",
        "destination_aqi_status": aqi_category(dst_aqi) if dst_aqi else "N/A"
    }
