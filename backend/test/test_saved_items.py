from fastapi.testclient import TestClient
from app.main import app
from app.repositories.users_repo import load_all as load_users
from app.repositories.products_repo import load_all as load_products

client = TestClient(app)

def _any_user_id() -> str:
    users = load_users()
    return users[0]["user_id"]


def _any_product_id() -> str:
    products = load_products()
    assert len(products) > 0
    p0 = products[0]
    for key in ("id", "product_id", "asin"):
        if key in p0:
            return p0[key]
    raise KeyError(f"Couldnt find product id key in product: {p0.keys()}")

def test_save_item_adds_id():
    user_id = _any_user_id()
    product_id = _any_product_id()
    r = client.post(f"/users/{user_id}/saved-items/{product_id}")
    assert r.status_code == 200, r.json()
    data = r.json()
    assert product_id in data["saved_item_ids"]

def test_save_item():
    user_id = _any_user_id()
    product_id = _any_product_id()
    client.post(f"/users/{user_id}/saved-items/{product_id}")
    r = client.post(f"/users/{user_id}/saved-items/{product_id}")
    assert r.status_code == 200, r.json()
    saved = r.json()["saved_item_ids"]
    assert saved.count(product_id) == 1

