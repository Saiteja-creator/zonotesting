import pytest
from controllers.features.order import *
from controllers.features.random_operations import generate_random_number


@pytest.fixture
def order_class(setup):
    order=Orders(setup)
    return order


@pytest.fixture
def get_pofile_details(order_class,workspaces_data):
    payload = {}
    # get_track_po_response for pofile_details
    track_po_res = order_class.get_track_po(workspaces_data, payload)
    OrderAssertion.verify_response_code_with_201(track_po_res)

    length = len(track_po_res.json["files"])
    generate_random_number_res = generate_random_number(length - 1)

    single_track_pofile = track_po_res.json["files"][generate_random_number_res]

    payload = {
        "pofileId": single_track_pofile["id"]
    }

    # pofile_details_res
    pofile_details = order_class.get_pofile_details(workspaces_data, payload)
    return pofile_details




class TestPurchaseOrderDetails:
    def test_get_pofile_Details(self,workspaces_data,order_class):
        payload={}
        #get_track_po_response for pofile_details
        track_po_res = order_class.get_track_po(workspaces_data,payload)
        OrderAssertion.verify_response_code_with_201(track_po_res)

        length = len(track_po_res.json["files"])
        generate_random_number_res = generate_random_number(length - 1)

        single_track_pofile = track_po_res.json["files"][generate_random_number_res]
        payload = {
            "pofileId": single_track_pofile["id"]
        }

        #pofile_details_res
        pofile_details = order_class.get_pofile_details(workspaces_data,payload)
        OrderAssertion.verify_response_code_with_201(pofile_details)
        # logger.error(f"single_track_pofile_details{single_track_pofile}")
        # logger.error(f"pofile_detials{pofile_details.json}")


        assert single_track_pofile["id"] == pofile_details.json["pofileId"]
        assert single_track_pofile["number"] == pofile_details.json["poNumber"]
        #assert single_track_pofile["skuCount"] == int(pofile_details.json["skuCount"])


    def test_search_pofile_details(self,workspaces_data,order_class,get_pofile_details):
        product_title = get_pofile_details.json["lines"]
        length = len(product_title)
        generate_random_number_res = generate_random_number(length - 1)
        sku_code = product_title[generate_random_number_res]["productVariant"]["translations"][0]["name"]



        payload = {
            "pofileId":get_pofile_details.json["pofileId"],
            "searchKey": "393939393"
        }
        search_purchase_details_res = order_class.get_pofile_details(workspaces_data,payload)



    def test_pofile_filter_by_submitted(self,get_pofile_details,order_class,workspaces_data):
        payload = {
          "pofileId": get_pofile_details.json["pofileId"],
          "filter": {
              "status": ["ORDER_SUBMITTED"]
          }
        }

        search_order_submitted = order_class.get_pofile_details(workspaces_data,payload)
















