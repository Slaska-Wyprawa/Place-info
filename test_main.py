from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_place_name():
    response = client.get("/place/sztolnia")
    assert response.status_code == 200
    assert response.json() == {"heritage": "2", "heritage:operator": "nid",
                               "name": "Główna Kluczowa Sztolnia Dziedziczna", "name:de": "Hauptschlüssel-Erbstollen",
                               "name:pl": "Główna Kluczowa Sztolnia Dziedziczna", "ref:nid": "A/220/07 z 11.12.2007",
                               "tourism": "attraction", "wikidata": "Q11708267",
                               "wikipedia": "pl:Główna Kluczowa Sztolnia Dziedziczna"}


def test_get_wrong_place_name():
    response = client.get("/place/test_dom")
    assert response.status_code == 404
