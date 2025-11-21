from app.services.preview_service import parse_to_previews
from app.schemas.product_preview import ProductPreview

TEST_PRODUCTS = [
    {"product_id":"1",
"product_name":"Pname 1",
"category":["cat1"],
"discounted_price":100.0,
"actual_price":1099.0,
"discount_percentage":"64%",
"rating":4.2,
"rating_count":24269,
"about_product":"about1",
"user_id":[],
"user_name":[],
"review_id":[],
"review_title":[],
"review_content":"",
"img_link":"https://not-a-link.com/img",
"product_link":"www.amazon.ca/"
},
{"product_id":"2",
"product_name":"Pname 2",
"category":["cat2"],
"discounted_price":200.0,
"actual_price":299.0,
"discount_percentage":"64%",
"rating":3.9,
"rating_count":6924,
"about_product":"about2",
"user_id":[],
"user_name":[],
"review_id":[],
"review_title":[],
"review_content":"",
"img_link":"https://not-a-link.com/img",
"product_link":"www.amazon.ca/"
},
{"product_id":"3",
"product_name":"Pname 3",
"category":["cat1","cat2"],
"discounted_price":300.0,
"actual_price":310.0,
"discount_percentage":"64%",
"rating":2.3,
"rating_count":52,
"about_product":"about3",
"user_id":[],
"user_name":[],
"review_id":[],
"review_title":[],
"review_content":"",
"img_link":"https://not-a-link.com/img",
"product_link":"www.amazon.ca/"
},
{"product_id":"4",
"product_name":"Pname 4",
"category":["cat4"],
"discounted_price":400.0,
"actual_price":800.0,
"discount_percentage":"50%",
"rating":4.5,
"rating_count":38792,
"about_product":"about1",
"user_id":[],
"user_name":[],
"review_id":[],
"review_title":[],
"review_content":"",
"img_link":"https://not-a-link.com/img",
"product_link":"www.amazon.ca/"
}
]


def test_parse_to_previews():
    previews = parse_to_previews(TEST_PRODUCTS)
    assert len(previews) == 4 #should not add or lose products when making previews
    for i in previews: #check all previews are valid
        assert isinstance(i,ProductPreview)
        assert isinstance(i.product_name,str)
        assert isinstance(i.product_id,str)
        assert isinstance(i.discounted_price,float)
        assert isinstance(i.rating,float)
