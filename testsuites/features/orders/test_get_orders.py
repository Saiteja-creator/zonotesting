import json

import pytest

from controllers.features.order import *
from controllers.api_util.random_operations import *

@pytest.fixture
def order_obj(setup):
    order=Orders(setup)
    return order

@pytest.fixture
def get_single_reOrder(order_obj, workspaces_data):
    get_order = order_obj.get_orders(workspaces_data)
    length = len(get_order.json["order"]) - 1
    generate_number = generate_random_number(length)
    single_order_id = get_order.json["order"][generate_number]["id"]
    get_single_order_details = order_obj.get_single_order_details(workspaces_data, single_order_id)


    return get_single_order_details

class TestOrders:

    def test_get_orders(self,setup,workspaces_data):
        orderObj=Orders(setup)
        get_order=orderObj.get_orders(workspaces_data)
        OrderAssertion.verify_response_code_with_201(get_order)


        assert get_order.json["order"], "Assertion failure verify_get_order body{}".format(get_order.json)


    def test_get_reOrder(self,test_pofile_checkout,get_single_reOrder,order_obj,workspaces_data):

        products = get_single_reOrder.json["lines"]
        list_products = []
        for i in get_single_reOrder.json["lines"]:                 #single order details and get each product productVariantId & Quantity for reOrder
            dict_a={}
            dict_a["productVariantId"] = i["productVariant"]["id"]
            dict_a["quantity"] =i["quantity"]
            list_products.append(dict_a)


        source_data = "manual"
        add_to_cart_res=order_obj.add_to_cart(workspaces_data,list_products,source_data)  # add_to_cart method

        Unavailable_products=[]
        if len(add_to_cart_res.json["errors"]) != 0:
            for i in add_to_cart_res.json["error"]:
                assert i["msg"] =="Product not found","msg Failure"
                Unavailable_products.append(i["productVariantId"])

        get_pofile_details=order_obj.get_pofiles(workspaces_data)           #response from get_pofile details

        assert len(add_to_cart_res.json["orders"]) > 0 , "No product add to the cart"

        get_pofile_response_manual_reOrder=[]
        for i in get_pofile_details.json["files"]:
            if i["importSource"] == "manual" and i["id"] == add_to_cart_res.json["orders"][0]["pofileId"]:

                for j in i["lines"]:
                    dict_b={}
                    dict_b["productVariantId"] = j["productVariantId"]
                    dict_b["quantity"] = j["quantity"]
                    get_pofile_response_manual_reOrder.append(dict_b)

      
      
        #verify order_details product add to cart
        for i in list_products:
            assert i in get_pofile_response_manual_reOrder, "Assertion Failure, Verify Is each order_details product add_to_cart"


        list_products_product_variant=[]
        for i in list_products:
            list_products_product_variant.append(i["productVariantId"])

        #verify, Unavailable product
        for j in Unavailable_products:
            assert j["productVariantId"] not in list_products_product_variant

















