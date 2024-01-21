
from controllers.features.product import *
def test_product_filter_id(setup,workspaces_data,return_product):

    product_class=Product(setup)
    productVariantId=return_product.product_data.json["products"][0]["productVariants"][0]["productVariantId"]
    addition_sort = {
        "productVariantId": productVariantId
    }
    product_obj = product_class.get_filter_product_data(workspaces_data,addition_sort)

    ProductAssertion.verify_response_code_with_201(product_obj)
    assert product_obj.json["products"][0]["productVariants"][0]["productVariantId"]==productVariantId,"Assertion failure verify product_variantId"
    ProductAssertion.verify_single_product(product_obj)


def test_product_filter_search_name(setup,workspaces_data,return_product):
    product_class = Product(setup)
    search_key=return_product.product_data.json["products"][0]["productVariants"][0]["name"]

    filter_data={
    "searchKey": search_key
    }
    product_search_res=product_class.get_filter_product_data(workspaces_data,filter_data)

    ProductAssertion.verify_response_code_with_201(product_search_res)
    assert product_search_res.json["products"][0]["productVariants"][0][
               "name"] == search_key, "Assertion failure verify search_product_name"
    ProductAssertion.verify_single_product(product_search_res)

def test_product_filter_search_sku(setup,workspaces_data,return_product):
    product_class = Product(setup)
    search_key = return_product.product_data.json["products"][0]["productVariants"][0]["sku"]
    filter_data = {
        "searchKey": search_key
    }
    product_search_res = product_class.get_filter_product_data(workspaces_data, filter_data)
    ProductAssertion.verify_response_code_with_201(product_search_res)
    assert product_search_res.json["products"][0]["productVariants"][0][
               "sku"] == search_key, "Assertion failure verify search_product_sku"
    ProductAssertion.verify_single_product(product_search_res)



