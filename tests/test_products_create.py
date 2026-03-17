from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product_valid_inputs():

    data = {
        "name": "Ben Tennyson",
        "strengths": "Compassionate and Responsible"
    }

    response = client.post("/products", json = data)
    assert response.status_code == 201

    data = {
        "name": " hi  ",
        "strengths": "oks f"
    }
    response = client.post ("/products", json = data)
    assert response.status_code == 201


def test_create_product_dublicate():

    data = {
        "name": "Ichigo Kurosaki",
        "strengths": "Compassionate and Protective"
    }

    response = client.post("/products", json  = data)
    assert response.status_code == 201

    response = client.post("/products", json = data)
    assert response.status_code == 409

def test_invalid_input():

    data = {
        "name": "",
        "strenghts": "ok"
    }

    response = client.post("/products", json = data)
    assert response.status_code == 422

    data = {
        "name": "   ",
        "strengths": "    "
    }
    response = client.post("/products", json = data)
    assert response.status_code == 422

def test_product_missing_field():

    data = {
        "name": "MissingStrength",
    }

    response = client.post("/products", json = data)
    assert response.status_code == 422