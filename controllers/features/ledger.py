import pytest
import json

from datetime import datetime
from urllib.parse import quote



current_date = datetime.now()


formatted_date = current_date.strftime("%Y-%m-%d")

from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *


class Ledger(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def get_ledger(self,workspaces_data,params=None):

        default_params = {
            "endDate" : f"{formatted_date}"
        }
        default_params.update(params)


        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]
        stringData = {"transactionType": ["INV"]}




        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/invoiceservice/partyAccountBook/list?sellerWorkspaceId={principal_workSpaceId}&inviteId={invite_workspaceId}&startDate=2024-01-08",
            params=default_params
        )
        return res


    def get_ledger_res(self,workspaces_data,params=None):

        default_params = {
            "endDate" : f"{formatted_date}"
        }
        default_params.update(params)


        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]


        stringData = {"transactionType": ["INV"]}
        encoded_object = quote(f"transactionType=['INV']", safe='')

        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/invoiceservice/partyAccountBook/balanceBySeller?sellerWorkspaceId={principal_workSpaceId}&inviteId={invite_workspaceId}&startDate=2024-01-09&endDate=2024-02-08&filter=%7B%22transactionType%22:%5B%22INV%22%5D%7D&includeOpeningBalance=true",
            # params={
            #     "endDate": "2024-02-08",
            #     "filter": encoded_object
            # }
        )
        return res







    def balance_by_seller_res(self,workspaces_data):
        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]
        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/invoiceservice/partyAccountBook/balanceBySeller?sellerWorkspaceId={principal_workSpaceId}&inviteId={invite_workspaceId}&startDate=2024-01-08&endDate={formatted_date}&filter=&includeOpeningBalance=true",
        )
        return res















class LedgerAssertion(BaseAssertion):
    pass