from fastapi.testclient import TestClient
from httpx import _status_codes
from app.main import app

client = TestClient(app)

def test_count_products():

    r1 = client.post("/products", json = {"name": "A test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C test", "strengths": "CS Test"})
    
    assert r1.status_code == r2.status_code == r3.status_code == 201

    response1 = client.get("/products/count")
    assert response1.status_code == 200

    count = response1.json()["data"]["count"]
    
    assert count == 3