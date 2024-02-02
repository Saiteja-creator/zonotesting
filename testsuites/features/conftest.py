from controllers.features.order import *

@pytest.fixture
def test_pofile_checkout(setup,workspaces_data):
    orderObj = Orders(setup)
    order_pofile = orderObj.get_pofiles(workspaces_data)
    data_manual = []
    for i in order_pofile.json["files"]:
        if i["importSource"] == "manual":
            data_manual.append(i["id"])
    #check the previous manual order
    orderObj.check_out(data_manual,workspaces_data)
    #get pofiles data
    update_pofile = orderObj.get_pofiles(workspaces_data)

    data_clear_manual_order=[]
    for k in update_pofile.json["files"]:
        if k["importSource"] == "manual":
            data_manual.append(k["id"])
    # data_clear_manual_order should be empty

    return data_clear_manual_order

@pytest.fixture
def add_to_cart(test_pofile_checkout,return_product,workspaces_data,setup):
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


