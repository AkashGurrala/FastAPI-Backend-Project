from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_products_list_no_filter():

    data1 = {"name": "Naruto Uzumaki", "strengths": "Chakra"}
    data2 = {"name": "Madara Uchiha", "strengths": "Sharingan"}

    r1 = client.post("/products", json = data1)
    r2 = client.post("/products", json = data2)

    
    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]

    response = client.get("/products")
    assert response.status_code == 200

    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert id1 in ids
    assert id2 in ids

def test_get_products_min_id_filter():
    r1 = client.post("/products", json = {"name": "A0 test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B0 test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C0 test", "strengths": "CS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    response4 = client.get(f"/products?min_id={id2}")

    assert response4.status_code == 200

    products = response4.json()["data"]
    ids = [p["id"] for p in products]

    assert id1 not in ids
    assert id2 in ids
    assert id3 in ids

    response5 = client.get("/products?min_id=abc")
    assert response5.status_code == 422

def test_get_products_sort_by_id():
    r1 = client.post("/products", json = {"name": "A1 test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B1 test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C1 test", "strengths": "CS Test"})
    r4 = client.post("/products", json = {"name": "D1 test", "strengths": "DS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]
    id4 = r4.json()["data"]["id"]

    response = client.get("/products?sort_by_product=True")

    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert ids ==  sorted(ids)

def test_get_products_name_contains():
    r1 = client.post("/products", json = {"name": "A2 test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "BA2 test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C2 test", "strengths": "CS Test"})
    
    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    response = client.get("/products?name_contains=A2")
    assert response.status_code == 200

    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert id1 in ids
    assert id2 in ids
    assert id3 not in ids

def test_get_products_limit():
    r1 = client.post("/products", json = {"name": "A3 test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B3 test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C3 test", "strengths": "CS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]
    
    response = client.get("/products?limit=2")
    assert response.status_code == 200
    
    products = response.json()["data"]
    assert len(products) == 2

    for p in products:
        assert "id" in p

    response = client.get("/products?limit=-2")
    assert response.status_code == 400 

    response = client.get("/products?limit=101")
    assert response.status_code == 400


def test_get_products_offset():
    response_all = client.get("/products")
    assert response_all.status_code == 200
    all_products = response_all.json()["data"]
    total_len = len(all_products)

    response = client.get("/products?offset=2")
    assert response.status_code == 200
    
    products = response.json()["data"]
    assert len(products) == max(total_len - 2, 0)

    response = client.get("/products?offset=-1")
    assert response.status_code == 400

def test_get_products_limit_offset():
    response_all = client.get("/products")
    assert response_all.status_code == 200

    all_products = response_all.json()["data"]
    total_len = len(all_products)

    limit = 2
    offset = 2

    response = client.get(f"/products?limit={limit}&offset={offset}")
    assert response.status_code == 200
    
    paginated = response.json()["data"]
    expected_len = min(limit, max(total_len - offset, 0))
    assert len(paginated) == expected_len

def test_get_products_min_id_limit():
    r1 = client.post("/products", json = {"name": "A4 test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B4 test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C4 test", "strengths": "CS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    limit = 2

    response = client.get(f"/products?min_id={id2}&limit={limit}")
    assert response.status_code == 200

    products = response.json()["data"]
    list_len = len(products)
    assert list_len == limit
    assert products[0]["id"] == id2