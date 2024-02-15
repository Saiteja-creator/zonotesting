from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *


class SettingCls(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def get_notification_res(self,workspaces_data):
        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        #principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        # invite_workspaceId = workspaces_data["inviteId"]



        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/hub/communication-v2/api/channels/app/communication/{client_workSpaceId}?sellerWorkspaceId={client_workSpaceId}",

        )
        return res

    def update_notification_res(self,workspaces_data,payload=None):
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]
        client_workSpaceId = workspaces_data["clientWorkspaceId"]

        default_payload = {
           "workspaceId" : client_workSpaceId,
            "sellerWorkspaceId" : principal_workSpaceId
        }
        default_payload.update(payload)

        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/hub/communication-v2/api/channels/app/communication/{client_workSpaceId}",
            payload=default_payload

        )
        return res







class SettingAssertions(BaseAssertion):
    pass