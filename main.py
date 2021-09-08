from functools import lru_cache

import httpx
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from fastapi import FastAPI, HTTPException, Depends, Response
from sqlmodel import Session, select

from config.config import Settings
from database import models
from database.database import engine

OSMApi = Api()
app = FastAPI()
nominatim = Nominatim()


@lru_cache()
def get_settings():
    return Settings()


@app.get("/place/{place_id}")
async def get_osm_place_info(place_id):
    with Session(engine) as session:
        osm_place_id = session.exec(select(models.Object.OPMapLink).where(models.Object.ObjectId == place_id)).first()
        if not osm_place_id:
            raise HTTPException(status_code=404, detail="OSM ID not found")
        place = OSMApi.query(f"way/{osm_place_id}")
        return place.tags()


@app.get("/address/{place_id}")
async def get_address(place_id):
    with Session(engine) as session:
        lat = session.exec(select(models.Object.Latitude).where(models.Object.ObjectId == place_id)).first()
        if not lat:
            raise HTTPException(status_code=404, detail="Latitude not found")
        lon = session.exec(select(models.Object.Longitude).where(models.Object.ObjectId == place_id)).first()
        if not lon:
            raise HTTPException(status_code=404, detail="Latitude not found")
        place = nominatim.query(lat, lon, reverse=True)
        return place


@app.get("/directions/start={start}&stop={stop}")
async def get_directions(response: Response, start, stop, settings: Settings = Depends(get_settings)):
    api_key = settings.open_route_api_key
    async with httpx.AsyncClient() as client:
        route = await client.get(f"https://api.openrouteservice.org/v2/directions/driving-car?"
                                 f"api_key={api_key}&start={start}&end={stop}")
        response.body = route.content
        response.status_code = route.status_code
        return response
