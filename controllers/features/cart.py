import pytest
import json

from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *

class Cart(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def get_pofiles(self,workspaces_data):
        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"https://api-uat.beta.pharmconnect.com/commerce-v2/poFiles/{workspaces_data["principalWorkspaceId"]}?customerId={workspaces_data["inviteId"]}&includeActiveOrders=true&includeSummary=true",

        )
        return res

    def delete(self,pofileId,pofileLineId,workspaces):
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/commerce-v2/orders/deleteLines/{workspaces["principalWorkspaceId"]}",
            payload={
                "customerId": workspaces["inviteId"],
                "sellerWorkspaceId": workspaces["principalWorkspaceId"],
                "poFileLineId": pofileId,
                "source": "manual",
                "lines": pofileLineId
            }
        )

        return res



