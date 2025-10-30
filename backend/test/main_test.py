from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    result = client.get("/hello")
    assert result.status_code == 200
    assert result.json() == {"msg": "Hello World"}

from app.services.product_service import get_product_by_id
def test_get_by_id():
    #Test getting a product by id and that its rating count matches value from json
    result = get_product_by_id("B082LZGK39")
    assert result.rating_count == "43,994"

def test_invalid_id():
    #Test an invalid id
    import pytest
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        get_product_by_id("42")