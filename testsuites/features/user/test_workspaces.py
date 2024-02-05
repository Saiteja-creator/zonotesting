import json

from controllers.features.users import *
import pytest
import logging
def test_workspaces_get_users(setup):
    result = setup.workspaces
    UsersAssertion.verify_general_response_code_200(result)
    assert result.json[0]["id"], "Assertion failure verify_workspaces_id body{}".format(result.json)
    assert result.json[0]["principal"], "Assertion failure verify principal data body{}".format(result.json)
    UsersAssertion.verify_workspaces(result)




