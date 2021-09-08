from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_get_osm_place_info():
    response = client.get("/place/1")
    assert response.status_code == 200
    assert response.json() == {
        "addr:city": "Zabrze",
        "addr:housenumber": "410",
        "addr:postcode": "41-800",
        "addr:street": "Wolności",
        "name": "Sztolnia Królowa Luiza",
        "operator": "Muzeum Górnictwa Węglowego w Zabrzu",
        "tourism": "theme_park",
        "website": "https://www.sztolnialuiza.pl/"
    }


def test_get_wrong_place_name():
    response = client.get("/place/22231")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "OSM ID not found"
    }


def test_get_address():
    response = client.get("/address/1")
    assert response.status_code == 200
    assert response.json() == {
        "_json": [
            {
                "place_id": 184392168,
                "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                "osm_type": "way",
                "osm_id": 421787802,
                "lat": "50.29627445",
                "lon": "18.806930225464242",
                "display_name": "Sztolnia Królowa Luiza, 410, Wolności, Zaborze Południe, Zabrze, "
                                "Górnośląsko-Zagłębiowska Metropolia, województwo śląskie, 41-800, Polska", 
                "address": {
                    "tourism": "Sztolnia Królowa Luiza",
                    "house_number": "410",
                    "road": "Wolności",
                    "city_district": "Zaborze Południe",
                    "city": "Zabrze",
                    "state_district": "Górnośląsko-Zagłębiowska Metropolia",
                    "state": "województwo śląskie",
                    "postcode": "41-800",
                    "country": "Polska",
                    "country_code": "pl"
                },
                "boundingbox": [
                    "50.2953218",
                    "50.297211",
                    "18.8055386",
                    "18.8079178"
                ]
            }
        ],
        "_queryString": "reverse",
        "_params": {
            "lat": 50.2957,
            "lon": 18.8062
        }
    }


def test_get_wrong_address():
    response = client.get("/address/512312")
    assert response.status_code == 404


def test_get_directions():
    response = client.get("/directions/start=8.681495,49.41461&stop=8.687872,49.420318")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["type"] == "FeatureCollection"
