import json

from controller.example_feature.users import *
import pytest
import logging


@pytest.fixture(scope="function", autouse=True)
def prepare_params(setup):
    setup.logic_controller = Users(setup)
    return setup
    pass


class TestGetUsers:
    def test_send_otp(self,prepare_params):

        result = prepare_params.otp
        assert result["temptoken"]

    def test_verify_otp(self,prepare_params):
        result=prepare_params.token
        assert result!=None

    def test_rat_get_users(self, setup):
        result = setup.workspaces
        UsersAssertion.verify_general_response_code_200(result)
        UsersAssertion.verify_workspaces(result)
        logging.info('setup.token args: %s', setup.workspaces)



