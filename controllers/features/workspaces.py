import pytest
import os
from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *
from controllers.api_util.file_operation import *

class Workspaces(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def principal_order_summary(self,workspaces_data):
        principal_id = workspaces_data["principalWorkspaceId"]
        invited_id = workspaces_data["inviteId"]
        customer_workspace=workspaces_data["clientWorkspaceId"]
        res = self.send_request(
            Base.RequestMethod.POST,

            custom_url=f"{self.settings.url_prefix}/commerce-v2/orders/order-scheme-summary/{principal_id}?customerId={invited_id}",
            payload={
                "sellerWorkspaceId": principal_id,
                "customerWorkspaceId": customer_workspace,
            }

        )

        return res




