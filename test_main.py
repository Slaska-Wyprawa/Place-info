from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_info():
    response = client.get("/place/sztolnia")
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
    response = client.get("/place/test_dom")
    assert response.status_code == 404


def test_get_address():
    response = client.get("/address/sztolnia")
    assert response.status_code == 200
    assert response.json() == {'_json': [
        {'place_id': 139221661, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright',
         'osm_type': 'way', 'osm_id': 202692683, 'lat': '50.29570875', 'lon': '18.806103131597553',
         'display_name': '408, Wolności, Zaborze Południe, Zabrze, Górnośląsko-Zagłębiowska Metropolia, województwo '
                         'śląskie, 41-806, Polska',
         'address': {'house_number': '408', 'road': 'Wolności', 'city_district': 'Zaborze Południe', 'city': 'Zabrze',
                     'state_district': 'Górnośląsko-Zagłębiowska Metropolia', 'state': 'województwo śląskie',
                     'postcode': '41-806', 'country': 'Polska', 'country_code': 'pl'},
         'boundingbox': ['50.2954637', '50.2959421', '18.8055446', '18.8066599']}], '_queryString': 'reverse',
                               '_params': {'lat': 50.29566, 'lon': 18.8062}}
