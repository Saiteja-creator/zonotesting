import pytest
import json

from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *
from controllers.api_util.date import *
from controllers.api_util.date import *

class Orders(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings = settings


    def get_orders(self,workspaces_data,payload):
        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]
        default_payload={
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
    "startDate": "2024-07-22T16:19:50+05:30",
    "endDate": "2024-08-22T16:19:50+05:30",
    "searchKeyword": "",
    "filterModel": {
        "divisionIds": [],
        "headDivisionIds": [],
        "cfaIds": [],
        "status": [],
        "customerIds": []
    },
    "includeProductInfo": True,
    "includeCFA":True ,
    "includeDivision": True
}
        
        default_payload.update(payload)




        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f'{self.settings.url_prefix}/hub/commerce-v2/orders?sellerWorkspaceId={principal_workSpaceId}&customerWorkspaceId={workspaces_data["clientWorkspaceId"]}&workspaceId={workspaces_data["principalWorkspaceId"]}',
            payload=default_payload
        )
        return res

    def get_single_order_details(self, workspaces_data,single_order_id):
        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]


        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f'{self.settings.url_prefix}/hub/commerce-v2/orders/details/{principal_workSpaceId}/{single_order_id}?includeInvoice=True&sellerWorkspaceId={principal_workSpaceId}',
            payload={
                "filter": {
                    "divisionIds": []
                },
                "searchKey": "",
                "includeInvoice": True,
                "includeTax": True,
                "includePromotions": True,
                "sortDirection": "DESC",
                "sortBy": "",
                "customerId": invite_workspaceId
            }
        )
        return res





    def add_to_cart(self,workspaces,product_data,source_data):

        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f'{self.settings.url_prefix}/hub/commerce-v2/orders/additemtoactiveorder/{workspaces["principalWorkspaceId"]}?sellerWorkspaceId={workspaces["principalWorkspaceId"]}',
            payload={
                "customerId": workspaces["inviteId"],
                "sellerWorkspaceId": workspaces["principalWorkspaceId"],
                "poFileLineId": None,
                "source": source_data,
                "lines": product_data
            }
        )
        return res

    def check_out(self,pofileList,workspaces):


        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f'{self.settings.url_prefix}/hub/commerce-v2/orders/checkout/{workspaces["principalWorkspaceId"]}?sellerWorkspaceId={workspaces["principalWorkspaceId"]}',
            payload={
                "sellerWorkspaceId": workspaces["principalWorkspaceId"],
                "customerId": workspaces["inviteId"],
                "poFileIds": pofileList
            }
        )
        return res

    def get_pofiles(self,workspaces_data):
        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/hub/commerce-v2/poFiles/{workspaces_data["principalWorkspaceId"]}?sellerWorkspaceId={workspaces_data["principalWorkspaceId"]}&customerId={workspaces_data["inviteId"]}&includeActiveOrders=True&includeSummary=True",

        )
        return res

    def get_track_po(self,workspaces_data,payload=None):
        default_payload={
            "customerId": workspaces_data["inviteId"],
            "includeSummary": True,
        }
        default_payload.update(payload)


        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/hub/commerce-v2/trackPoFiles/{workspaces_data["principalWorkspaceId"]}?sellerWorkspaceId={workspaces_data["principalWorkspaceId"]}",
            payload=default_payload

        )
        return res



    def get_pofile_details(self,workspaces_data,payload=None):
        default_payload={
            "includeInvoice": True,
            "includePromotion": True,
            "includeTax": True
        }
        default_payload.update(payload)


        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/hub/commerce-v2/pofiles/details/{workspaces_data["principalWorkspaceId"]}?sellerWorkspaceId={workspaces_data["principalWorkspaceId"]}",
            payload=default_payload

        )
        return res

    def get_download(self,workspaces_data,pofileId):
        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/poFile/download/{workspaces_data["principalWorkspaceId"]}?pofileId={pofileId}",

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
        return data_list




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
