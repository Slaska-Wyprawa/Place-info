from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from fastapi import FastAPI, HTTPException

OSMApi = Api()
app = FastAPI()
nominatim = Nominatim()

places = {
    "sztolnia": {
        "id": "421787802",
        "lat": 50.29566,
        "lon": 18.80620
    }
}


@app.get("/place/{place}")
async def get_info(place):
    if place in places:
        place = OSMApi.query(f"way/{places.get(place).get('id')}")
        return place.tags()
    else:
        raise HTTPException(status_code=404, detail="Place not found")


@app.get("/address/{place}")
async def get_address(place):
    if place in places:
        place = nominatim.query(places.get(place).get('lat'), places.get(place).get('lon'), reverse=True)
        return place
    else:
        raise HTTPException(status_code=404, detail="Place not found")
