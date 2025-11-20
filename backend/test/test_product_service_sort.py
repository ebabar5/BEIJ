from unittest.mock import patch #use unittest
import pytest
from fastapi import HTTPException

from app.services.product_service import list_products

SAMPLE_PRODUCTS = [
    {
        "product_id": "random",
        "product_name": "New Product",
        "category": ["shoes"],
        "discounted_price": 10.0,
        "actual_price": 20.0,
        "discount_percentage": "50%",
        "rating": 4.0,
        "rating_count": 5,
        "about_product": "desc",
        "user_id": ["u1"],
        "user_name": ["User 1"],
        "review_id": ["r1"],
        "review_title": ["Nice"],
        "review_content": "ok",
        "img_link": "http://random.com/a",
        "product_link": "http://random.com/a",
    },
    {
        "product_id": "random2",
        "product_name": "Old Product",
        "category": ["shoes"],
        "discounted_price": 30.0,
        "actual_price": 10.0,
        "discount_percentage": "25%",
        "rating": 4.0,
        "rating_count": 10,
        "about_product": "desc",
        "user_id": ["u1"],
        "user_name": ["User 1"],
        "review_id": ["r2"],
        "review_title": ["Good"],
        "review_content": "ok",
        "img_link": "http://random.com/b",
        "product_link": "http://random.com/b",
    },
]

@patch("app.services.product_service.load_all")
def test_list_products_sort_by_price_asc(mock_load_all):
    mock_load_all.return_value = SAMPLE_PRODUCTS

    products = list_products(sort_by="price_asc")
    prices = [p.discounted_price for p in products]
    assert prices == sorted(prices) #check if sorted by ascending 


@patch("app.services.product_service.load_all")
def test_list_products_invalid_sort_raises_error(mock_load_all):
    mock_load_all.return_value = SAMPLE_PRODUCTS

    with pytest.raises(HTTPException) as exc_info:
        list_products(sort_by="not_a_real_option")
    assert exc_info.value.status_code == 400