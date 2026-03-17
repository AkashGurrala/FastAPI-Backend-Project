from fastapi.testclient import TestClient
from app.main import app

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
    
    fetch_response = client.get(f"/product/9999")

    assert fetch_response.status_code == 404
    res = fetch_response.json()
    print(res)
    print(res["detail"])
    assert "not found" in res["detail"].lower()
