from controllers.features.order import *


def test_get_orders(setup,workspaces_data):
    orderObj=Orders(setup)
    get_order=orderObj.get_orders(workspaces_data)
    OrderAssertion.verify_response_code_with_201(get_order)
    assert get_order.json["order"], "Assertion failure verify_get_order body{}".format(get_order.json)


