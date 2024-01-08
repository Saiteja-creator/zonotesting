import pytest

from controller.api_util.base_request import Base, BaseAssertion
from controller.api_util.common_imports import *

class Product(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def get_Product(self,workspaces_data):
        principal_id = workspaces_data["principalWorkspaceId"]
        invited_id = workspaces_data["inviteId"]
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/products/search/{principal_id}?pageNo=1&pageSize=20&customerId={invited_id}",
            payload={}
        )
        return res



    #get_filter_product_data()
    #get_on_click_product_data()



class ProductAssertion(BaseAssertion):
    @classmethod
    def verify_specific_results(cls, res: Base.ResponseObject):
        pass
        # Here to verify specific results from Response Object

