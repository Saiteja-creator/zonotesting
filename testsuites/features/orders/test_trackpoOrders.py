

from controllers.features.order import *


@pytest.fixture(scope="module")
def order_class(setup):
    order = Orders(setup)
    return order


@pytest.fixture(scope="class")
def get_track_po_res(order_class,workspaces_data):
    payload = {}
    get_track_po = order_class.get_track_po(workspaces_data,payload)

    return get_track_po


class TestOrderTrackPO:
    def test_track_pores(self,get_track_po_res):
        OrderAssertion.verify_response_code_with_201(get_track_po_res)
        assert get_track_po_res.json["summary"],"Assertion Failure, Verify get_trackPo summary"


    #search by po_number
    def test_search_po(self,get_track_po_res,order_class,workspaces_data):
        files_details=get_track_po_res.json["files"]

        po_number = None
        for i in files_details:
            if i["number"] != None:
                po_number = i["number"]
                break

        #if po_number is not found
        if po_number==None:
            po_number = "0303030"

        payload = {
            "searchKey": po_number
        }

        get_search_res=order_class.get_track_po(workspaces_data,payload)

        OrderAssertion.verify_response_code_with_201(get_search_res)

        for i in get_search_res.json["files"]:
            assert po_number in i["number"]

    def test_filter_by_cfa(self, get_track_po_res,order_class,workspaces_data):
        get_cfa = get_track_po_res.json["summary"]["cfas"][0]["fullFillmentLocationId"]

        payload = {
            "filterParams": [get_cfa]
        }

        filter_cfa_res = order_class.get_track_po(workspaces_data,payload)

        filter_cfa_summary = filter_cfa_res.json["summary"]["cfas"]

        verify_cfa = False
        for i in filter_cfa_summary:
            if get_cfa == i["fullFillmentLocationId"]:
                verify_cfa = True
        assert verify_cfa




















