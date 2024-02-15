import json
from controllers.features.users import *
import pytest
import logging

@pytest.fixture
def prepare_paramas(setup):
    userData=Users(setup)

class TestGetUsers:


    def test_send_otp(self,setup):
        res=setup.otp
        UsersAssertion.verify_general_response_code_200(res)
        UsersAssertion.verify_tempToken(res)
        UsersAssertion.verify_mfaStatus(res)
        UsersAssertion.verify_mobile_otp(res)

        if res.json["mfaStatus"]==True:

            UsersAssertion.verify_email_otp(res)


    def test_verify_otp(self,setup):
        res =setup.token

        UsersAssertion.verify_general_response_code_200(res)
        UsersAssertion.verify_token(res)
        assert res.json["mobile"] == str(setup.dataset["users"]["mobile"]), "Assertion failure verify mobile No "








