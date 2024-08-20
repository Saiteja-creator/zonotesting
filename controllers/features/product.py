import pytest
import os
from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *
from controllers.api_util.file_operation import *

class Product(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings


    def get_Product(self,workspaces_data):
        principal_id = workspaces_data["principalWorkspaceId"]
        invited_id = workspaces_data["inviteId"]
        res = self.send_request(
            Base.RequestMethod.POST,

            custom_url=f"{self.settings.url_prefix}/hub/commerce-v2/products/search/{principal_id}?sellerWorkspaceId={principal_id}&pageNo=1&pageSize=20&customerId={invited_id}",
            payload={},

        )
       

        return res

    def get_filter_product_data(self,workspaces_data,addition_args):
        principal_id = workspaces_data["principalWorkspaceId"]
        invited_id = workspaces_data["inviteId"]

        payload_json_data = {}

        payload_json_data.update(addition_args)
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/hub/commerce-v2/products/search/{principal_id}?sellerWorkspaceId={principal_id}&pageNo=1&pageSize=20&customerId={invited_id}",
            payload=payload_json_data
        )


        return res






class ProductAssertion(BaseAssertion):
    @classmethod
    def verify_specific_results(cls, res: Base.ResponseObject):
        pass
        # Here to verify specific results from Response Object
    @classmethod
    def verify_total_product(cls, res: Base.ResponseObject):
        cls.log_assert(res.json["total"] != None, "Assertion Failure, verify total, body: {}".format(res.json))


    @classmethod
    def verify_single_product(cls,res: Base.ResponseObject):
        cls.log_assert(res.json["total"]>=1, "Assertion failure verify get_single_product body{}".format(res.json))



