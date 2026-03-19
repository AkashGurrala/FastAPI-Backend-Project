from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_fetch_product_by_id_success():

    data = {
        "name": "Sasuke Uchiha",
        "strengths": "Talent and Strong Will"
    }
    create_response = client.post("/products", json = data)
    assert create_response.status_code == 201

    created = create_response.json()
    product_id = created["data"]["id"]

    fetch_response = client.get(f"/products/{product_id}")
    assert fetch_response.status_code == 200

    fetched = fetch_response.json()["data"]

    assert fetched["id"] == product_id
    assert fetched["name"] == "Sasuke Uchiha"
    assert fetched["strengths"] == "Talent and Strong Will"

def test_fetch_product_by_id_no_product_found():
    
    fetch_response = client.get(f"/products/9999")
    assert fetch_response.status_code == 404

    res = fetch_response.json()
    assert "no product found" in res["message"].lower()

@pytest.mark.parametrize("invalid_id", [0,-1])
def test_fetch_product_by_id_invalid_input(invalid_id):

    response = client.get(f"/products/{invalid_id}")
    assert response.status_code == 400

def test_fetch_product_by_id_invalid_type():

    response = client.get("/products/abc")
    assert response.status_code == 422