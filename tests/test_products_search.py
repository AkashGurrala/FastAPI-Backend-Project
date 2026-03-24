from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_string_contains():
    r1 = client.post("/products", json = {"name": "X0A1 test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "Y0A1 test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "Z test", "strengths": "CS Test"})
    
    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    response = client.get("/products/search?string=0A1")
    assert response.status_code == 200

    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert len(products) == 2
    assert set(ids) == {id1, id2}