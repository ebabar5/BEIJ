from test.dummy_data.dummy_products import TEST_PRODUCTS
from app.services.filtering import filter_product_list

def test_filter_category():
    cat_string1 = "cat1" #products 1 and 3 have this category
    cat_string2 = "cat3" #none of the test products have this category
    cat_string3 = "cat2*cat4"

    #Check that the filter pull correctly from products with single and multiple categories
    result1 = filter_product_list(TEST_PRODUCTS,cat_string1)
    assert len(result1) == 2
    #The filter should not reorder the list, just remove what doesn't meet the filter
    assert result1[0]["product_id"] == "1"
    assert result1[1]["product_id"] == "3"

    #check behaviour with no matching categories
    result2 = filter_product_list(TEST_PRODUCTS,cat_string2)
    assert len(result2) == 0

    #Check the the filter handles filtering multiple categories
    result3 = filter_product_list(TEST_PRODUCTS,cat_string3)
    assert len(result3) == 3
    assert result3[0]["product_id"] == "2"
    assert result3[2]["product_id"] == "4"
                     
def test_filter_price():
    #Test the max price filtering
    max1 = 200
    result1 = filter_product_list(TEST_PRODUCTS,"",max_price=max1)
    assert len(result1) == 2
    for i in result1:
        assert i["discounted_price"] <= max1

    #Test the min price filtering
    min2 = 250
    result2 = filter_product_list(TEST_PRODUCTS,"",min_price=min2)
    assert len(result2) == 2
    for j in result2:
        assert j["discounted_price"] >= min2

    #Test filtering both and min/max flip handling
    result3 = filter_product_list(TEST_PRODUCTS,"all",min_price=250,max_price=125)
    assert result3[0]["product_id"] == "2"
