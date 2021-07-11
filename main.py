from OSMPythonTools.api import Api
from fastapi import FastAPI, HTTPException

OSMApi = Api()
app = FastAPI()

places = {
    "sztolnia": 165513542
}


@app.get("/place/{name}")
async def get_place_name(name):
    if name in places:
        place = OSMApi.query(f"way/{places.get(name)}")
        return place.tags()
    else:
        raise HTTPException(status_code=404, detail="Place not found")
