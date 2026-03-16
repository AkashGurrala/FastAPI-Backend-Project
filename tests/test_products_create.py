from fastapi.testclient import TestClient
from app.api.routes import products
from app.main import app

client = TestClient(app)

def test_create_product():

    data = {
        "name": "Ben Tennyson",
        "strengths": "Compassionate and Responsible"
    }

    response = client.post("/products", json = data)

    assert response.status_code == 201

    res = response.json()
    product = res["data"]
    assert res["status"] == "success"
    assert product["name"] == "Ben Tennyson"
    assert product["strengths"] == "Compassionate and Responsible"

