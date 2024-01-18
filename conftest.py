
import pytest
import logging
from controllers.settings import Settings

from controllers.features.users import Users

from controllers.features.product import Product

from controllers.features.scheme import Scheme

from controllers.features.order import *




def pytest_addoption(parser):
    parser.addoption('--env', action='store',
                     help='setup environment; STAGING, PROD')
    parser.addoption('--dataset', action='store',
                     help='setup name of test data set (ex: test_data_set_1)')
    parser.addoption('--disable_ssh_tunnel', action='store_true', default=False,
                     help='Setup SSH Tunnel to connect with MongoDB (ex: True=1 or False=0)')
    parser.addoption('--settings_file', action='store', default=None,
                     help='setup settings data (ex: AIXON , EDP ; Default is AIXON)')
    parser.addoption("--api_version", action="store", metavar="api_version", default=None,
                     help="only run tests matching the api version as api_version.")


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line("markers",
                            "version(number): mark test to run only on named version")




@pytest.fixture(scope="session",autouse=True)
def setup(request):
    setup = Settings(request)
    setup.logic_controller = Users(setup)
    setup.otp = setup.logic_controller.send_otp()

    if (setup.otp.json["mfaStatus"]):
        setup.mobile_otp = setup.logic_controller.verify_mobile_otp(setup.otp)
        setup.token = setup.logic_controller.verify_email_otp(setup.otp,setup.mobile_otp)
    else:
        setup.token = setup.logic_controller.verify_otp(setup.otp)

    setup.logic_controller = Users(setup)
    setup.workspaces = setup.logic_controller.get_workspaces()

    yield setup


@pytest.fixture(scope="session")
def workspaces_data(setup):
    workspaces_data=(setup.logic_controller.get_workspaces()).json

    principal_dict = {}
    for i in (workspaces_data):
        for j in (i["principal"]):
            principal_dict = j
    logging.info(f"it's returns the principal_data {principal_dict}")

    return principal_dict

@pytest.fixture(scope="session")
def return_product(setup,workspaces_data):
    product = Product(setup)
    product.product_data = product.get_Product(workspaces_data)
    return product

@pytest.fixture(scope="session")
def return_scheme(setup,workspaces_data):
    scheme = Scheme(setup)
    scheme.get_scheme_data = scheme.get_scheme(workspaces_data["principalWorkspaceId"])

    return scheme

@pytest.fixture(scope="module")
def return_orders(setup,workspaces_data,return_product):

    product_data_order=return_product.product_data
    orders = Orders(setup)
    orders.get_orders_data = orders.get_orders(workspaces_data)

    orders.add_to_cart_res = orders.add_to_cart(workspaces_data,product_data_order)
    orders.check_out_res = orders.check_out(orders.add_to_cart_res.json,workspaces_data)

    return orders


@pytest.fixture(scope="session")
def return_upload_order(setup,workspaces_data,return_product):
    upload_order=UploadOrders(setup)
    upload_order.upload_order = upload_order.upload_order(workspaces_data)
    upload_order.upload_add_order = upload_order.upload_add_order(workspaces_data, upload_order.upload_order)
    upload_order.upload_checkout = upload_order.upload_checkout(workspaces_data, upload_order.upload_add_order.json)


    return upload_order


def pytest_runtest_setup(item):
    version_marker = item.get_closest_marker("version")
    assigned_version = item.config.getoption("--api_version")
    if version_marker:
        version = version_marker.args[0]
        if not item.config.getoption("--api_version"):
            logging.warning("Not assigned api_version argument, but test case requires version as {}"
                            .format(version))
        elif version != assigned_version:
            pytest.skip(
                "test requires running on api version {}".format(version))
    else:
        logging.warning("Not found marker of the api version")
        logging.warning("Run test case by assigned api version as {}".format(
            assigned_version if assigned_version else Settings.DEFAULT_API_VERSION))

