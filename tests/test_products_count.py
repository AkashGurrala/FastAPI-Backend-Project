from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_count_products():
    response1 = client.get("/products/count")
    assert response1.status_code == 200

    count = response1.json()["data"]["count"]
    
    response2 = client.get("/products")
    total_count = len(response2.json()["data"])
     
    assert count == total_count