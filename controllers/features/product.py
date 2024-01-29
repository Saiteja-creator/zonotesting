import pytest
import os
from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *
from controllers.api_util.file_operation import *

class Product(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings
        self.cur_file_dir=os.path.dirname(os.path.realpath(__file__))

    def get_Product(self,workspaces_data):
        principal_id = workspaces_data["principalWorkspaceId"]
        invited_id = workspaces_data["inviteId"]
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/products/search/{principal_id}?pageNo=1&pageSize=100&customerId={invited_id}",
            payload={}
        )
        # logger.warning(f"response of get_product {res.json}")



        return res

    def get_filter_product_data(self,workspaces_data,addition_args):
        principal_id = workspaces_data["principalWorkspaceId"]
        invited_id = workspaces_data["inviteId"]
        payload_template = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','data', 'product.json'))
        payload_json_data = read_json(payload_template)

        if addition_args:
            payload_json_data.update(addition_args)
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/products/search/{principal_id}?pageNo=1&pageSize=20&customerId={invited_id}",
            payload=payload_json_data
        )
        logger.warning(f"response of get_product {res.json}")

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
        cls.log_assert(res.json["total"]==1, "Assertion failure verify get_single_product body{}".format(res.json))



