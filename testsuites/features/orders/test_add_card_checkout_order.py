
from controllers.features.order import *


@pytest.fixture
def test_add_to_cart(return_product,workspaces_data,setup):
    orderObj = Orders(setup)
    product_data_order = return_product.product_data
    add_to_cart_res=orderObj.add_to_cart(workspaces_data, product_data_order)

    OrderAssertion.verify_response_code_with_201(add_to_cart_res)
    assert add_to_cart_res.json["orders"]
    assert add_to_cart_res.json["orders"][0]["importSource"] == "manual", "Assertion failure verify_manual_order body{}".format(add_to_cart_res.json)

    return add_to_cart_res


def test_checkout(test_add_to_cart,setup,workspaces_data):
    orderObj = Orders(setup)
    check_out_res = orderObj.check_out(test_add_to_cart.json, workspaces_data)
    OrderAssertion.verify_response_code_with_201(check_out_res)


