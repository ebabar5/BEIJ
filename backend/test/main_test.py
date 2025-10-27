from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    result = client.get("/hello")
    assert result.status_code == 200
    assert result.json() == {"msg": "Hello World"}

from app.services.items_service import get_item_by_id
def test_get_by_id():
    #Test getting the "Soccer Balls" item id=="2"
    result = get_item_by_id("2")
    assert result.title == "Soccer Balls"

def test_invalid_id():
    #Test an invalid id
    import pytest
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        get_item_by_id("42")