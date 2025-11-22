import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.services.product_service import get_product_by_id

@pytest.fixture
def client():
    return TestClient(app)

def test_home(client):
    result = client.get("/hello")
    assert result.status_code == 200
    assert result.json() == {"msg": "Hello World"}

def test_get_by_id():
    result = get_product_by_id("B082LZGK39")
    assert isinstance(result.rating_count, int)
    assert result.rating_count == 43994

@pytest.mark.parametrize("bad_id", ["42"])
def test_invalid_id(bad_id):
    with pytest.raises(HTTPException):
        get_product_by_id(bad_id)
