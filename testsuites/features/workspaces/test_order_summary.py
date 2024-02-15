import pytest

from controllers.features.workspaces import *
from controllers.features.order import *

@pytest.fixture
def workspace_obj(setup):
    workspace = Workspaces(setup)
    return workspace


@pytest.fixture
def order_obj(setup):
    orders=Orders(setup)
    return orders




class TestWorkspaces:
    def test_order_summary(self,return_scheme,workspace_obj,workspaces_data,order_obj):
        order_summary_res=workspace_obj.principal_order_summary(workspaces_data)
        order_summary_response_json=order_summary_res.json

        #verify principalWorkspacesId and code  from worksapces response
        assert  workspaces_data["principalWorkspaceId"] == order_summary_response_json["workSpaceId"], "Assertion Failure, sellerWorkspaceId"
        assert order_summary_response_json["code"] == workspaces_data["code"], 'Assertion Failure, Principal name'


        #verify total_orders, Start with createdDate from workspace date
        assert workspaces_data["createdDate"]
        principal_workspaces_date = workspaces_data["createdDate"][:10]
        payload={
            "startDate" : principal_workspaces_date
        }

        # get orders from startDate(workspace's CreateDate) to end_date
        get_orders = order_obj.get_orders(workspaces_data,payload)
        assert get_orders.json["totalRecords"] == int(order_summary_response_json["totalOrders"]), "Assertion Failure, Verify total_orders with get_order_summary"

        # verify active Schemes
        get_scheme_response = return_scheme.get_scheme_data
        assert get_scheme_response.json["totalRecords"] == int(order_summary_response_json["schemeCount"]), "Assertion Failure, Verify Active Schemes"








