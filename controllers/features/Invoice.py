import pytest
import json

from datetime import datetime,timedelta

current_date = datetime.now()


last_month_date = current_date - timedelta(days=current_date.day)


formatted_last_month_date = last_month_date.replace(day=1, hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")


formatted_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *


class Invoice(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def get_invoice(self,workspaces_data,params):
        default_params = {
            "endDate": f"{formatted_date}",

        }
        default_params.update(params)


        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]
        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/invoiceservice/invoices/{principal_workSpaceId}?&startDate=2024-01-09%2000%3A00%3A00&inviteId={invite_workspaceId}",
            params=default_params
        )
        return res

    def invoices_aggregated(self,workspaces_data):
        default_params = {
            "endDate": f"{formatted_date}",
            "startDate": f"{formatted_last_month_date}"
        }
        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]
        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/invoiceservice/invoices/aggregated/{principal_workSpaceId}?",
            params=default_params
        )
        return res

    def single_invoice(self,workspaces_data,invoice_id):
        default_params = {
            "endDate": f"{formatted_date}",
            "startDate": f"{formatted_last_month_date}"
        }

        principal_workSpaceId = workspaces_data["principalWorkspaceId"]

        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/invoiceservice/invoice/{invoice_id}?includePayment=true&workspaceId={principal_workSpaceId}",
            params=default_params
        )
        return res

    def invoice_download(self,workspaces_data,payload_value):
        default_payload = {
            "endDate": f"{formatted_date}",
            "startDate": f"{formatted_last_month_date}"

        }
        default_payload.update(payload_value)

        principal_id = workspaces_data["principalWorkspaceId"]
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/invoiceservice/invoices/download/{principal_id}",
            payload=default_payload,

        )
        return res








class InvoiceAssertion(BaseAssertion):
    pass
