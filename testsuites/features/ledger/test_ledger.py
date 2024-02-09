import json

import pytest

from controllers.features.ledger import *
from controllers.api_util.random_operations import *


@pytest.fixture(scope="session")
def ledger_obj(setup):
    ledger = Ledger(setup)
    return ledger

@pytest.fixture(scope="module")
def get_ledger_res(ledger_obj,workspaces_data):
    params={}
    get_ledger_res=ledger_obj.get_ledger(workspaces_data,params)
    return get_ledger_res

class TestLedger:
    # def test_get_ledger(self,ledger_obj,workspaces_data):
    #     params={}
    #     get_ledger_res=ledger_obj.get_ledger(workspaces_data,params)
    #     LedgerAssertion.verify_general_response_code_200(get_ledger_res)
    #     assert get_ledger_res.json["partyAccountBook"], "Assertion Failure,partyAccountBook"
    #     partyAccountBook_res = get_ledger_res.json["partyAccountBook"]
    #     assert len(partyAccountBook_res) > 0, "No data available"
    #
    #
    # def test_filter_search(self,ledger_obj,workspaces_data,get_ledger_res):
    #
    #     LedgerAssertion.verify_general_response_code_200(get_ledger_res)
    #
    #     partyAccountBook_res = get_ledger_res.json["partyAccountBook"]
    #     length = len(partyAccountBook_res)-1
    #     generate_random_no = generate_random_number(length)
    #     do_number = partyAccountBook_res[generate_random_no]["docNumber"][:3]
    #     params_data = {
    #         "searchKey": do_number
    #     }
    #
    #     get_search_ledger_res=ledger_obj.get_ledger(workspaces_data,params_data)
    #     LedgerAssertion.verify_general_response_code_200(get_search_ledger_res)
    #
    #     for i in get_search_ledger_res.json["partyAccountBook"]:
    #         assert do_number in i["docNumber"]


    def test_filter_purchase_invoice(self,get_ledger_res,ledger_obj,workspaces_data):
        partyAccountBook_res = get_ledger_res.json["partyAccountBook"]
        length = len(partyAccountBook_res) - 1
        generate_random_no = generate_random_number(length)
        transaction_type = partyAccountBook_res[generate_random_no]["transactionType"]


        params = {
            "filter": {"transactionType": ["INV"]}
        }

        get_ledger_res_purchase_invoice = ledger_obj.get_ledger_res(workspaces_data,params)
        # logger.error(f"Return the get_ledger_res{get_ledger_res_purchase_invoice.json}")


    def test_copy_ledger_filter(self,ledger_obj,workspaces_data):
        params={}
        ledger_res=ledger_obj.copy_get_ledger(workspaces_data,params)
        logger.error(f"return the ledger{ledger_res.json}")






    # def test_balance_seller(self,ledger_obj,workspaces_data):
    #     get_balance_ledger = ledger_obj.balance_by_seller_res(workspaces_data)
    #     LedgerAssertion.verify_general_response_code_200(get_balance_ledger)
    #
    #
    #



