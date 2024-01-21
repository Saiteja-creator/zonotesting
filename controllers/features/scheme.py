import pytest

from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *

class Scheme(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def get_scheme(self,principal_id):

        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/scheme/{principal_id}?pageNo=1&pageSize=20&skuCode=&sortDirection=&sortBy=&includeCFA=true&startDate=2023-12-05&endDate=2024-01-04&dispatchFilters=true&status=&promotionType=",
            payload={}
        )
        return res






    #get_filter_scheme()
    #get_filter_on_click_scheme()



class SchemeAssertion(BaseAssertion):
    @classmethod
    def verify_specific_results(cls, res: Base.ResponseObject):
        pass
        # Here to verify specific results from Response Object