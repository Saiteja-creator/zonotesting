
from controllers.features.order import *


@pytest.fixture
def test_add_to_cart(test_pofile_checkout,return_product,workspaces_data,setup):
    assert test_pofile_checkout==[],"assertion error, manual order checkout"
    product_Data_res = return_product.product_data.json
    data_list = []
    for i in product_Data_res["products"]:
        for j in i["productVariants"]:
            data_list.append(
                {"productVariantId": j["productVariantId"], "quantity": j["minOrderQty"], "operator": "add"})

    orderObj = Orders(setup)
    source="manual"

    add_to_cart_res = orderObj.add_to_cart(workspaces_data, data_list,source)
    checked_pofile_data=orderObj.get_pofiles(workspaces_data)

    OrderAssertion.verify_response_code_with_201(add_to_cart_res)

    assert checked_pofile_data.json["files"][-1]["importSource"] == "manual", "Assertion failure verify Cart of manual orders"

    assert add_to_cart_res.json["orders"][0]["orderLine"][0]["productVariantId"]
    assert add_to_cart_res.json["orders"][0]["orderLine"][0]["productVariantId"]== product_Data_res["products"][0]["productVariants"][0]["productVariantId"]
    assert add_to_cart_res.json["orders"][0]["importSource"] == "manual", "Assertion failure verify_manual_order body{}".format(add_to_cart_res.json)

    return add_to_cart_res




def test_checkout(test_add_to_cart,setup,workspaces_data):
    orderData=test_add_to_cart.json
    pofileList = []
    for i in orderData["orders"]:
        pofileList.append(i["pofileId"])
    orderObj = Orders(setup)
    check_out_res = orderObj.check_out(pofileList, workspaces_data)
    check_order_data=orderObj.get_orders(workspaces_data)
    #check Assertion is order add or not
    OrderAssertion.verify_response_code_with_201(check_out_res)




