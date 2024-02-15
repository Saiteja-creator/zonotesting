import pytest

from controllers.api_util.base_request import Base, BaseAssertion
from controllers.api_util.common_imports import *

class Users(Base):
    def __init__(self,settings):
        Base.__init__(self,settings)
        self.settings=settings

    def send_otp(self):
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/sendotp",
            payload={"authChannel": "mobile",
                     "mobile": self.settings.dataset['users']['mobile']}
        )
        return res

#
    def verify_otp(self, otp):

        otp=otp.json
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/verifyotp",
            payload={
                "authChannel": "mobile",
                "mobile": self.settings.dataset['users']['mobile'],
                "otp": str(otp["mobile"]["otp"])
            },
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {otp["temptoken"]}"}
        )
        return res


    def verify_mobile_otp(self,otp):
        otp = otp.json
        res = self.send_request(
            Base.RequestMethod.POST,
            custom_url=f"{self.settings.url_prefix}/verifyotp",
            payload={
                "authChannel": "mobile",
                "mobile": self.settings.dataset['users']['mobile'],
                "otp": str(otp["mobile"]["otp"]),
                "mfa_status": True
            },
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {otp["temptoken"]}"}
        )

        return res.json

    def verify_email_otp(self,otp,verify_mobile_otp):
        otp=otp.json
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

        return res


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
    def verify_tempToken(cls, res: Base.ResponseObject):
        cls.log_assert(res.json["temptoken"] != None,"Assertion Failure, verify temptoken, body:{}".format(res.json))

    @classmethod
    def verify_mfaStatus(cls, res: Base.ResponseObject):
        cls.log_assert(res.json["mfaStatus"] != None, "Assertion Failure, verify mfaStatus, body:{}".format(res.json))

    @classmethod
    def verify_mobile_otp(cls, res: Base.ResponseObject):
        cls.log_assert(len(str((res.json["mobile"]["otp"]))) == 4 , "Assertion Failure, verify_mobile_otp, body:{}".format(res.json))

    @classmethod
    def verify_email_otp(cls, res: Base.ResponseObject):
        cls.log_assert(len(str((res.json["mobile"]["otp"]))) == 4 , "Assertion Failure, verify_mobile_otp, body:{}".format(res.json))


    @classmethod
    def verify_token(cls,res: Base.ResponseObject):
        cls.log_assert(res.json["token"], "Assertion Failure, verify_token body{}.".format(res.json))



    @classmethod
    def verify_workspaces(cls, res: Base.ResponseObject):
        cls.log_assert(res.json[0]["isBuyer"] == True, "Assertion Failure, verify isBuyer, body: {}".format(res.json))

