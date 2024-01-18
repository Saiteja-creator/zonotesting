
from controllers.features.order import *

@pytest.fixture(scope="module")
def add_to_cart(return_product,workspaces_data,setup):
    orderObj = Orders(setup)
    product_data_order = return_product.product_data
    add_to_cart_res=orderObj.add_to_cart(workspaces_data, product_data_order)
    return add_to_cart_res
def test_add_cart(add_to_cart):
    pass

