from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# equivalence partitioning integration test 
def test_wide_and_strict_search_query():
    q = "arandomitemhere1"
    wide = client.get(f"/previews/search/w={q}")
    strict = client.get(f"/previews/search/{q}")

    assert wide.status_code == 200
    assert strict.status_code == 200
    assert wide.json() == strict.json()

# integration test for empty-search route 
def test_no_search_entry():
    resp = client.get("/previews/search/")

    assert resp.status_code == 200
    assert resp.json() == "Please enter a search query"
