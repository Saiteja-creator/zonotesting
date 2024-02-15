from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *



class MyAccount(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def get_account_details(self,workspaces_data):

        principal_workSpaceId = workspaces_data["principalWorkspaceId"]


        #logger.error(f"return the client_workspaceId{client_workSpaceId},prinicipal_workspaceId{principal_workSpaceId}, inivited_id{invite_workspaceId}")

        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/users/me/v2?includeCFA=true&sellerWorkspaceId={principal_workSpaceId}",

        )
        return res

    def update_myaccont(self,workspaces_data,payload=None):
        client_workSpaceId = workspaces_data["clientWorkspaceId"]
        principal_workSpaceId = workspaces_data["principalWorkspaceId"]
        invite_workspaceId = workspaces_data["inviteId"]
        # logger.error(f"return the client_workspaces{client_workSpaceId}, principal_workjspaces{principal_workSpaceId}, invite_workspaces{invite_workspaceId}")
        default_payload = {"workspaceId":client_workSpaceId}
        default_payload.update(payload)

        res = self.send_request(
            Base.RequestMethod.PUT,
            custom_url=f"{self.settings.url_prefix}/workspace/details",
            payload=default_payload

        )
        return res

    def get_user_profile(self,payload):
        res = self.send_request(
            Base.RequestMethod.PUT,
            custom_url=f"{self.settings.url_prefix}/users",
            payload=payload

        )
        return res

    def workspaces_document(self,pdf_file):

        file_path = r"C:\Users\91954\Downloads\gst_doc-document (2).pdf"

        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"https://api-qa.beta.pharmconnect.com/workspaces/documents/bb7da722-37cb-4e6e-a07c-0efbb4c75ca8",
            payload={
                    "documentType": "customer",
                    "entityId": "gst_doc-bb7da722-37cb-4e6e-a07c-0efbb4c75ca8",
                    "mimeType": "application/pdf",
                    "subType": "gst_doc",
                    "sequenceNo": "1"
                },

        )

        return res




