from unittest.mock import patch #use unittest
import pytest
from fastapi import HTTPException

from app.services.product_service import list_products
from test.dummy_data.dummy_products import SAMPLE_PRODUCTS

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