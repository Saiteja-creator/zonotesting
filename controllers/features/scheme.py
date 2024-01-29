import pytest

from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *

class Scheme(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def get_scheme(self,workspaces_data):
        principal_id=workspaces_data["principalWorkspaceId"]

        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/scheme/{principal_id}?pageNo=1&pageSize=20&skuCode=&sortDirection=&sortBy=&includeCFA=true&startDate=2023-12-05&endDate=2025-01-04&dispatchFilters=true&status=&promotionType=",
            payload={}
        )
        return res

    def get_scheme_code(self,scheme_code,workspaces_data):
        principal_id = workspaces_data["principalWorkspaceId"]

        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/scheme/{principal_id}/{scheme_code}",
        )
        return res

    def get_scheme_filter(self,workspaces_data,filter_data=None,payload_value=None):
        default_filters = {
            "pageNo": 1,
            "pageSize": 20
        }
        default_filters.update(filter_data)
        principal_id = workspaces_data["principalWorkspaceId"]
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/scheme/{principal_id}?&includeCFA=true&startDate=&endDate=",
            params=default_filters,
            payload=payload_value
        )

        return res







    #get_filter_scheme()
    #get_filter_on_click_scheme()



class SchemeAssertion(BaseAssertion):
    @classmethod
    def verify_specific_results(cls, res: Base.ResponseObject):
        pass
        # Here to verify specific results from Response Object