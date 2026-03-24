from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_products_list_no_filter():

    data1 = {"name": "Naruto Uzumaki", "strengths": "Chakra"}
    data2 = {"name": "Madara Uchiha", "strengths": "Sharingan"}

    r1 = client.post("/products", json = data1)
    r2 = client.post("/products", json = data2)

    assert r1.status_code == r2.status_code == 201
    
    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]

    response = client.get("/products")
    assert response.status_code == 200

    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert set(ids) == {id1, id2}

def test_get_products_min_id_filter():
    r1 = client.post("/products", json = {"name": "A test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C test", "strengths": "CS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    response4 = client.get(f"/products?min_id={id2}")

    assert response4.status_code == 200

    products = response4.json()["data"]
    ids = [p["id"] for p in products]

    assert set(ids) == {id2, id3}

    response5 = client.get("/products?min_id=abc")
    assert response5.status_code == 422

def test_get_products_sort_by_id():
    r1 = client.post("/products", json = {"name": "A test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C test", "strengths": "CS Test"})
    r4 = client.post("/products", json = {"name": "D test", "strengths": "DS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]
    id4 = r4.json()["data"]["id"]

    response = client.get("/products?sort_by_id=True")

    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert ids ==  [id1, id2, id3, id4]

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

    assert set(ids) == {id1, id2}

def test_get_products_limit():
    r1 = client.post("/products", json = {"name": "A test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C test", "strengths": "CS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    response = client.get("/products?limit=2&sort_by_id=True")
    assert response.status_code == 200
    
    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert ids == [id1, id2]

    response = client.get("/products?limit=-2")
    assert response.status_code == 400 

    response = client.get("/products?limit=101")
    assert response.status_code == 400


def test_get_products_offset():
    r1 = client.post("/products", json = {"name": "A test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C test", "strengths": "CS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    response = client.get("/products?offset=1&sort_by_id=True")
    assert response.status_code == 200
    
    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert ids == [id2, id3]

    response = client.get("/products?offset=-1")
    assert response.status_code == 400

def test_get_products_limit_offset():
    r1 = client.post("/products", json = {"name": "A test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C test", "strengths": "CS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    limit = 2
    offset = 1

    response = client.get(f"/products?limit={limit}&offset={offset}&sort_by_id=True")
    assert response.status_code == 200
    
    products = response.json()["data"]
    ids = [p["id"] for p in products]

    assert ids == [id2, id3]

def test_get_products_min_id_limit():
    r1 = client.post("/products", json = {"name": "A test", "strengths": "AS Test"})
    r2 = client.post("/products", json = {"name": "B test", "strengths": "BS Test"})
    r3 = client.post("/products", json = {"name": "C test", "strengths": "CS Test"})

    id1 = r1.json()["data"]["id"]
    id2 = r2.json()["data"]["id"]
    id3 = r3.json()["data"]["id"]

    limit = 2

    response = client.get(f"/products?min_id={id2}&limit={limit}&sort_by_id=True")
    assert response.status_code == 200

    products = response.json()["data"]
    ids = [p["id"] for p in products]
    
    assert len(products) == limit
    assert ids == [id2, id3]