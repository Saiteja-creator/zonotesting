import pytest

from controller.api_util.base_request import Base, BaseAssertion
from controller.api_util.common_imports import *

class Users(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def send_otp(self):
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/sendotp",
            payload={"authChannel": "mobile",
                     "mobile": self.settings.dataset['user']['mobile']}
        )
        return res.json


#
    def verify_otp(self, otp):
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/verifyotp",
            payload={
                "authChannel": "mobile",
                "mobile": self.settings.dataset['user']['mobile'],
                "otp": str(otp["mobile"]["otp"])
            },
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {otp["temptoken"]}"}
        )
        return res.json["token"]


    def verify_mobile_otp(self,otp):

        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/verifyotp",
            payload={
                "authChannel": "mobile",
                "mobile": self.settings.dataset['user']['mobile'],
                "otp": str(otp["mobile"]["otp"]),
                "mfa_status": True
            },
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {otp["temptoken"]}"}
        )

        return res.json

    def verify_email_otp(self,otp,verify_mobile_otp):
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/verifyotp",
            payload={
                "authChannel": "email",
                "email": verify_mobile_otp["email"],
                "otp": str(otp["email"]["otp"]),
                "mfa_status": True
            },
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {verify_mobile_otp["temptoken"]}"}
        )

        return res.json["token"]


    def get_workspaces(self):
        res = self.send_request(
            Base.RequestMethod.GET,
            custom_url=f"{self.settings.url_prefix}/workspaces",

        )
        return res





class UsersAssertion(BaseAssertion):
    @classmethod
    def verify_specific_results(cls, res: Base.ResponseObject):
        pass
        # Here to verify specific results from Response Object
    @classmethod
    def verify_workspaces(cls,res: Base.ResponseObject):
        cls.log_assert(res.json[0]["isBuyer"] == True,"Assertion Failure, verify token, body: {}".format(res.text))

