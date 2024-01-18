import pytest
import json

from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *

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

class UploadOrders(Base):
    def __init__(self, settings):
        Base.__init__(self, settings)
        self.settings = settings


    def upload_order(self,workspaces):
        customer_url=f"{self.settings.url_prefix}/commerce-v2/poFile/upload/{workspaces["principalWorkspaceId"]}"

        file_path = r"C:\Users\91954\Downloads\RAJASTHAN DRUG HOUSE.xlsx"
        #file_path = r"C:\Users\91954\Downloads\UAT PO.xlsx"
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/poFile/upload/{workspaces["principalWorkspaceId"]}",
            params = {
                    'customerId': workspaces["inviteId"],
                    'importSource': 'upload',
                    'parserType': 'C2D_ORDER'
                },
            headers={},
            files = {'file': open(file_path, 'rb')}

        )

        return res

    def upload_add_order(self,workspaces,upload_order_data):

        up_data = upload_order_data.json

        poFile = None
        data_list = []
        data_unmapped=[]
        for i in up_data:
            if i["status"] == "MAPPED":
                data_list.append(
                    {"productVariantId": i["productVariantId"], "quantity": i["unitQuantity"], "poFileLineId": i["id"]})
                poFile = i["poFileId"]
            else:
                data_unmapped.append(i)
        for each_map in data_unmapped:

            resUnmapped = self.send_request(
                Base.RequestMethod.POST,
                custom_url=f"{self.settings.url_prefix}/commerce-v2/products/search/{workspaces["principalWorkspaceId"]}?customerId={workspaces["inviteId"]}&pageNo=1&pageSize=20",
                payload={
                    "searchKey": each_map["uploadedProductName"],
                    "includeFacets": True,
                    "includeDivisions": True,
                    "includeCollections": True,
                    "includeCfas": True
                    }
            )

            response_unmapped=resUnmapped.json

            if response_unmapped["total"]!=0:
                value_quantity=each_map["unitQuantity"]
                quantity = value_quantity if value_quantity>0 else response_unmapped["products"][0]["productVariants"][0]["minOrderQty"]

                unmaped_object={"productVariantId": response_unmapped["products"][0]["productVariants"][0]["productVariantId"], "quantity": quantity, "poFileLineId": each_map["id"]}

                data_list.append(unmaped_object)


        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/orders/additemtoactiveorder/{workspaces["principalWorkspaceId"]}",
            payload={
            "customerId": workspaces["inviteId"],
            "sellerWorkspaceId":workspaces["principalWorkspaceId"],
            "source": "upload",
            "poFileId": poFile,
            "lines": data_list
            }
        )


        return res

    def upload_checkout(self,workspaces,upload_data):

        pofileList = []
        for i in upload_data["orders"]:
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







class OrderAssertion(BaseAssertion):
    @classmethod
    def verify_specific_results(cls, res: Base.ResponseObject):
        pass
        # Here to verify specific results from Response Object
