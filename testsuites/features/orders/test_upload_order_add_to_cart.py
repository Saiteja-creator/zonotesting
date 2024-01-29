import json

from controllers.features.order import *


@pytest.fixture
def test_upload_order(setup,workspaces_data):
    orderObj=UploadOrders(setup)
    upload_order_res=orderObj.upload_order(workspaces_data)


    OrderAssertion.verify_response_code_with_201(upload_order_res)
    assert upload_order_res.json[0]["status"]
    assert upload_order_res.json[0]["poFileId"]

    return upload_order_res

@pytest.fixture
def test_check_map_unmaped(setup,workspaces_data,test_upload_order):
    uploadorderObj=UploadOrders(setup)
    orderObj=Orders(setup)
    source="upload"
    upload_add_orders_res=uploadorderObj.upload_add_order(workspaces_data,test_upload_order)

    add_to_cart=orderObj.add_to_cart(workspaces_data,upload_add_orders_res,source)
    OrderAssertion.verify_response_code_with_201(add_to_cart)
    assert add_to_cart.json["orders"][0]["importSource"] == "upload", "Assertion failure verify importSource"
    assert upload_add_orders_res[0]["productVariantId"] == add_to_cart.json["orders"][0]["orderLine"][0]["productVariantId"],"Assertion failure, productVariantId"

    return add_to_cart


def test_upload_checkout(test_check_map_unmaped,workspaces_data,setup,totalWorkspaceData):
    orderData = test_check_map_unmaped.json

    pofileList = []
    for i in orderData["orders"]:
        pofileList.append(i["pofileId"])
    orderObj = Orders(setup)
    check_out_res = orderObj.check_out(pofileList, workspaces_data)
    check_order_data = orderObj.get_orders(workspaces_data)


    # check Assertion, is order add or not
    OrderAssertion.verify_response_code_with_201(check_out_res)

   #verify add_to_cart_res_id == get_order_data_id
    assert orderData["orders"][0]["id"] == check_order_data.json["order"][0]["id"],"Assertion failure, verify orders Id"

    #verify the add_to_cart_res_id == checkout_res_id
    assert orderData["orders"][0]["id"] == check_out_res.json["orders"][0]["id"], "Assertion failure, verify add_to_cart_id and verify_checkout_id"

    #verify checkout_id == get_order_id......
    assert check_out_res.json["orders"][0]["id"] == check_order_data.json["order"][0]["id"], "Assertion failure, verify check_out_id with get_order_id"

    #verify add_to_cart_Cfa,get_orders_cfa
    assert orderData["orders"][0]["CFA"]==check_order_data.json["order"][0]["orderMetaData"]["cfa"]

    #verify distributor
    assert totalWorkspaceData[0]["spaceName"] == check_order_data.json["order"][0]["customerName"]


    logger.error(f"return add_to_cart_data {orderData["orders"]}")
    logger.error(f"return get_checkout_res{check_out_res.json}")
    logger.error(f"return the get_orders list in upload{json.dumps(check_order_data.json["order"][0],indent=4)}")



