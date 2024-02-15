# import pytest
# import random
# import string
from controllers.features.Settings.myAccount import *
from controllers.features.users import *


@pytest.fixture(scope="module")
def pdf_file():
    # Path to your PDF file
    file_path = r"C:\Users\91954\Downloads\Book (6)_RAJ.pdf"
    with open(file_path, "rb") as f:
        yield f


@pytest.fixture
def account_obj(setup):
    my_account=MyAccount(setup)
    return my_account




list_a=[]


class TestMyAccount:


    def test_mandatory_field(self,account_obj,workspaces_data,setup):

        #response from users_me api
        get_myAccount_res=account_obj.get_account_details(workspaces_data)
        assert get_myAccount_res.status_code == 200, "Assertion Failure, Verify the status code"

        assert get_myAccount_res.json["email"], "Assertion Failure, Verify the user email"
        assert get_myAccount_res.json["firstName"], "Assertion Failure, Verify user firstName "
        assert get_myAccount_res.json["inviteDetails"]["phone"], "Assertion Failure, Verify  Mobile Number"

        #response from workspaces
        workspaces=setup.workspaces
        workspaces_response=workspaces.json[0]["businessDetails"]
        assert workspaces_response["gstin"], "Assertion Failure, Verify gstIn"
        assert workspaces_response["companyEmail"],"Assertion Failure, Verify company Email"
        assert workspaces_response["companyName"],"Assertion Failure, Verify companyName"

        #verify address
        address=workspaces_response["physicalAddress"]
        assert len(address) == 6 , "Assertion Failure, Verify length address filed"
        logger.error(f"return the address {address}")
        assert address["city"], "Assertion Failure, Verify user city"
        assert address["postcode"],"Assertion Failure, Verify user postcode"
        assert address["state"], "Assertion Failure, Verify user state"
        assert address["formatted"], "Assertion Failure, Verify user formatted"


    def test_update_workspaceDetails_api_fileds(self,account_obj,workspaces_data,setup):
        payload={}
        get_previous_myAccount_res=account_obj.get_account_details(workspaces_data)
        assert get_previous_myAccount_res.status_code == 200, "Assertion Failure, Verify the status code"

        payload={
        "physicalAddress": {
            "postcode": "205621",
            "city": "Hyderabad",
            "state": "Telengana",
            "neighborhood": "",
            "formatted": "Madhapur",
            "suburb": ""
        },
        "legalName": "RAJASTHAN DRUG HOUSE,llll",
        "companyRefCode": "",
        "timeZone": "Asia/Kolkata",
        "spaceName": "RAJASTHAN DRUG HOUSE",
        "companyEmail": "test143@gmail.com",

    }

        update_payload=account_obj.update_myaccont(workspaces_data,payload)

        get_update_response_res=account_obj.get_account_details(workspaces_data)
        assert get_update_response_res.status_code == 200
        assert get_update_response_res.status_code == 200

        assert get_previous_myAccount_res.json["email"] == get_update_response_res.json["email"]
        assert get_previous_myAccount_res.json["inviteDetails"]["phone"] == get_update_response_res.json["inviteDetails"]["phone"]

        #verify workspaces
        userCls=Users(setup)
        workspaces_response_data=userCls.get_workspaces()
        workspaces_data=workspaces_response_data.json[0]["businessDetails"]
        payload_res=payload["physicalAddress"]

        assert payload_res == workspaces_data["physicalAddress"], "Assertion Failure, Verify myAccount (address) update api payload with workspaces response"

        assert payload["legalName"] == workspaces_data["legalName"], "Assertion Failure, Verify company legalName"



    def test_update_user_api_field(self,workspaces_data,account_obj):
        payload={
            "firstName": "Rajasthanmm"
        }

        get_response_user=account_obj.get_user_profile(payload)
        assert get_response_user.status_code ==200
        assert get_response_user.json["data"]["firstName"] == payload["firstName"], "Assertion Failure, Update the user name"

        get_myAccount_res = account_obj.get_account_details(workspaces_data)
        assert get_myAccount_res.status_code == 200, "Assertion Failure, Verify the status code"

        assert get_myAccount_res.json["email"], "Assertion Failure, Verify the user email"

        assert get_myAccount_res.json["inviteDetails"]["phone"], "Assertion Failure, Verify  Mobile Number"


    def test_Gst_upload(self,account_obj,pdf_file):
        get_response_downaload=account_obj.workspaces_document(pdf_file)
        logger.error(f"return the get_response_download{get_response_downaload.json}")


