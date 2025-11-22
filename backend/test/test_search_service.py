from fastapi.testclient import TestClient
from app.main import app
from test.dummy_data.dummy_products import TEST_PRODUCTS
from app.services.search_service import keyword_search
from app.schemas.product import Product

client = TestClient(app)

def test_search_unfiltered():
    keywords = ["HDMI"]
    #Perform a strict search without filters
    result = keyword_search(keywords,True)
    assert len(result) > 0
    assert "HDMICables" in result[0]["category"]

def test_search_filtered():
    #Compare a filtered and unfiltered search to make sure the filter is eliminating results
    keywords = ["HDMI"]
    filtered = keyword_search(keywords,True,"Cables")
    unfiltered = keyword_search(keywords,True,)
    if len(unfiltered) != 0:
        assert len(filtered) < len(unfiltered)
    

#Test that the router calls the method and returns an expected result
def test_previews_search_routing():
    response = client.get("/api/v1/previews/search/4k&HDMICables")
    assert response.status_code == 200
    #Search is case insensitive so we need to check both 4k and 4K
    assert "4K" in response.json()[0]["product_name"] or "4k" in response.json()[0]["product_name"]