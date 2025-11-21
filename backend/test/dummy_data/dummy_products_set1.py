
# Sample data with varied values for comprehensive testing
SAMPLE_PRODUCTS = [
    {
        "product_id": "prod1",
        "product_name": "Zebra Shoes",
        "category": ["footwear"],
        "discounted_price": 50.0,
        "actual_price": 100.0,
        "discount_percentage": "50%",
        "rating": 4.5,
        "rating_count": 100,
        "about_product": "Great shoes",
        "user_id": ["u1"],
        "user_name": ["User One"],
        "review_id": ["r1"],
        "review_title": ["Excellent Quality"],
        "review_content": "Excellent",
        "img_link": "http://example.com/zebra.jpg",
        "product_link": "http://example.com/zebra"
    },
    {
        "product_id": "prod2", 
        "product_name": "Alpha Boots",
        "category": ["footwear"],
        "discounted_price": 75.0,
        "actual_price": 150.0,
        "discount_percentage": "50%",
        "rating": 4.8,
        "rating_count": 50,
        "about_product": "Premium boots",
        "user_id": ["u2"],
        "user_name": ["User Two"],
        "review_id": ["r2"],
        "review_title": ["Amazing Product"],
        "review_content": "Amazing",
        "img_link": "http://example.com/alpha.jpg",
        "product_link": "http://example.com/alpha"
    },
    {
        "product_id": "prod3",
        "product_name": "Beta Sneakers",
        "category": ["footwear"],
        "discounted_price": 25.0,
        "actual_price": 50.0,
        "discount_percentage": "50%",
        "rating": 3.9,
        "rating_count": 200,
        "about_product": "Comfortable sneakers",
        "user_id": ["u3"],
        "user_name": ["User Three"],
        "review_id": ["r3"],
        "review_title": ["Good Value"],
        "review_content": "Good value",
        "img_link": "http://example.com/beta.jpg",
        "product_link": "http://example.com/beta"
    }
]

# Products with identical ratings for tiebreaker testing
IDENTICAL_RATING_PRODUCTS = [
    {
        "product_id": "tie1",
        "product_name": "Product A",
        "category": ["test"],
        "discounted_price": 10.0,
        "actual_price": 20.0,
        "discount_percentage": "50%",
        "rating": 4.0,
        "rating_count": 100,  # Higher count should come first
        "about_product": "Test product",
        "user_id": ["u1"],
        "user_name": ["User"],
        "review_id": ["r1"],
        "review_title": ["Test Review"],
        "review_content": "Test",
        "img_link": "http://example.com/a.jpg",
        "product_link": "http://example.com/a"
    },
    {
        "product_id": "tie2",
        "product_name": "Product B",
        "category": ["test"],
        "discounted_price": 15.0,
        "actual_price": 30.0,
        "discount_percentage": "50%",
        "rating": 4.0,
        "rating_count": 50,   # Lower count should come second
        "about_product": "Test product",
        "user_id": ["u2"],
        "user_name": ["User"],
        "review_id": ["r2"],
        "review_title": ["Test Review"],
        "review_content": "Test",
        "img_link": "http://example.com/b.jpg",
        "product_link": "http://example.com/b"
    }
]