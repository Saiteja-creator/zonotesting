import pytest

from controller.api_util.base_request import Base, BaseAssertion
from controller.api_util.common_imports import *

class Orders(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings


    def get_orders(self,workspaces_data):

        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]

        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/orders?customerWorkspaceId={workspaces_data["clientWorkspaceId"]}&workspaceId={workspaces_data["principalWorkspaceId"]}",
            payload={
            "workspaceId": principal_workSpaceId,
            "customerId": invite_workspaceId,
            "pageNo": 1,
            "skip": 1,
            "pageSize": 20,
            "sortBy": "orderDate",
            "sortDirection": "DESC",
            "includeCustomer": True,
            "includeSummary": True,
            "includeInvoice": True,
            "includeStatus": True,
            "startDate": "2023-12-06",
            "endDate": "2024-01-05",
            "searchKeyword": "",
            "filterModel": {
            "divisionIds": [],
            "headDivisionIds": [],
            "cfaIds": [],
            "status": [],
            "customerIds": []
            },
            "includeProductInfo": True,
            "includeCFA": True,
            "includeDivision": True
            }
        )
        return res


    def add_to_cart(self,workspaces,product_data):
        product_Data=product_data.json
        data_list = []
        for i in product_Data["products"]:
            for j in i["productVariants"]:
                data_list.append({"productVariantId": j["productVariantId"],"quantity": j["minOrderQty"],"operator": "add"})


        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/orders/additemtoactiveorder/{workspaces["principalWorkspaceId"]}",
            payload={
                "customerId": workspaces["inviteId"],
                "sellerWorkspaceId": workspaces["principalWorkspaceId"],
                "source": "manual",
                "lines": data_list
            }
        )
        return res

    def check_out(self,orderData,workspaces):
        pofileList=[]
        for i in orderData["orders"]:

            pofileList.append(i["pofileId"])

        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/orders/checkout/{workspaces["principalWorkspaceId"]}",
            payload={
                "sellerWorkspaceId": workspaces["principalWorkspaceId"],
                "customerId": workspaces["inviteId"],
                "poFileIds": pofileList
            }
        )
        return res


    #add_to_cart()
    #check_out()



class OrderAssertion(BaseAssertion):
    @classmethod
    def verify_specific_results(cls, res: Base.ResponseObject):
        pass
        # Here to verify specific results from Response Object
