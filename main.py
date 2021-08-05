from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from fastapi import FastAPI, HTTPException, Depends, Response
from functools import lru_cache
import httpx

from config.config import Settings

OSMApi = Api()
app = FastAPI()
nominatim = Nominatim()

places = {
    "sztolnia": {
        "id": "421787802",
        "lat": 50.29566,
        "lon": 18.80620
    },
    "kamieniolom": {
        "id": "739500100",
        "lat": 50.18178,
        "lon": 18.84864
    }
}


@lru_cache()
def get_settings():
    return Settings()


@app.get("/place/{place}")
async def get_info(place):
    if place in places:
        place = OSMApi.query(f"way/{places.get(place).get('id')}")
        return place.tags()
    else:
        raise HTTPException(status_code=400, detail="Place not found")


@app.get("/address/{place}")
async def get_address(place):
    if place in places:
        lat = places.get(place).get('lat')
        lon = places.get(place).get('lon')
        place = nominatim.query(lat, lon, reverse=True)
        return place
    else:
        raise HTTPException(status_code=400, detail="Place not found")


@app.get("/directions/start={start}&stop={stop}")
async def get_directions(response: Response, start, stop, settings: Settings = Depends(get_settings)):
    api_key = settings.open_route_api_key

    @lru_cache()
    async def get_openrouteservice():
        async with httpx.AsyncClient() as client:
            # Coordinate of the route in longitude,latitude format.
            route = await client.get(f"https://api.openrouteservice.org/v2/directions/driving-car?"
                                     f"api_key={api_key}&start={start}&end={stop}")
            response.body = route.content
            response.status_code = route.status_code

    await get_openrouteservice()
    return response
