from controllers.features.order import *


@pytest.fixture
def test_upload_order(setup,workspaces_data):
    orderObj=UploadOrders(setup)
    upload_order_res=orderObj.upload_order(workspaces_data)

    OrderAssertion.verify_response_code_with_201(upload_order_res)
    return upload_order_res

@pytest.fixture
def test_check_map_unmaped(setup,workspaces_data,test_upload_order):
    uploadorderObj=UploadOrders(setup)
    orderObj=Orders(setup)
    source="upload"
    upload_add_orders_res=uploadorderObj.upload_add_order(workspaces_data,test_upload_order)

    add_to_cart=orderObj.add_to_cart(workspaces_data,upload_add_orders_res,source)
    OrderAssertion.verify_response_code_with_201(add_to_cart)

    assert upload_add_orders_res[0]["productVariantId"] == add_to_cart.json["orders"][0]["orderLine"][0]["productVariantId"],"Assertion failure, productVariantId"
    logger.error(f"return the upload_order_pofile_id{add_to_cart.json}")
    return add_to_cart


def test_upload_checkout(test_check_map_unmaped,workspaces_data,setup):
    orderData = test_check_map_unmaped.json
    pofileList = []
    for i in orderData["orders"]:
        pofileList.append(i["pofileId"])
    orderObj = Orders(setup)
    check_out_res = orderObj.check_out(pofileList, workspaces_data)
    check_order_data = orderObj.get_orders(workspaces_data)
    # check Assertion is order add or not
    OrderAssertion.verify_response_code_with_201(check_out_res)
