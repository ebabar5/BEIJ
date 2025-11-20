from app.services.preview_service import parse_to_previews
from app.schemas.product_preview import ProductPreview

from test.dummy_data.dummy_products import TEST_PRODUCTS


def test_parse_to_previews():
    previews = parse_to_previews(TEST_PRODUCTS)
    assert len(previews) == 4 #should not add or lose products when making previews
    for i in previews: #check all previews are valid
        assert isinstance(i,ProductPreview)
        assert isinstance(i.product_name,str)
        assert isinstance(i.product_id,str)
        assert isinstance(i.discounted_price,float)
        assert isinstance(i.rating,float)
