import json

import pytest

from controllers.features.Invoice import *
from controllers.api_util.random_operations import *

invoice_to_test = ["P", "PD", "PP", "C", "OD"]

@pytest.fixture
def invoice_obj(setup):
    invoice=Invoice(setup)
    return invoice


@pytest.fixture
def get_invoice_res(invoice_obj,workspaces_data):
    params = {}
    get_response_invoice = invoice_obj.get_invoice(workspaces_data, params)
    return get_response_invoice



class TestInvoice:
    def test_get_invoice_res(self,get_invoice_res):
        InvoiceAssertion.verify_general_response_code_200(get_invoice_res)
        assert get_invoice_res.json["invoices"], "Assertion Failure, Verify Invoice field"

    def test_search_invoice_do(self,get_invoice_res,invoice_obj,workspaces_data):
        invoice_data = get_invoice_res.json["invoices"]
        length = len(invoice_data)-1
        assert length>=0,"Assertion Failure,Invoice doesn't have any data"
        generate_no = generate_random_number(length)
        do_number = invoice_data[generate_no]["docNumber"][-3:]
        params = {
            "searchKey": do_number
        }
        response_search_invoice=invoice_obj.get_invoice(workspaces_data,params)
        for i in response_search_invoice.json["invoices"]:
            assert do_number in i["docNumber"]

    @pytest.mark.parametrize("each_params", invoice_to_test)
    def test_filter_Invoice(self,each_params,workspaces_data,invoice_obj):
        params = {
            "invoiceStatus": each_params
        }

        response = invoice_obj.get_invoice(workspaces_data,params)
        InvoiceAssertion.verify_general_response_code_200(response)

        for i in response.json["invoices"]:

           assert i["invoiceStatus"] == each_params


    def test_invoices_aggregated(self,invoice_obj,workspaces_data):
        response_data=invoice_obj.invoices_aggregated(workspaces_data)
        InvoiceAssertion.verify_general_response_code_200(response_data)


    def test_single_invoice_Data(self,get_invoice_res,invoice_obj,workspaces_data):
        invoice_data = get_invoice_res.json["invoices"]
        length = len(invoice_data) - 1
        assert length >= 0, "Assertion Failure,Invoice doesn't have any data"
        generate_no = generate_random_number(length)
        invoice_id = invoice_data[generate_no]["id"]
        get_single_invoice_res = invoice_obj.single_invoice(workspaces_data,invoice_id)
        InvoiceAssertion.verify_general_response_code_200(get_single_invoice_res)


    def test_invoice_download(self,invoice_obj,get_invoice_res,workspaces_data):
        invoice_data = get_invoice_res.json["invoices"]
        length = len(invoice_data) - 1
        generate_no = generate_random_number(length)
        invoice_id = invoice_data[generate_no]["id"]
        payload = {
            "invoiceIds": [
                invoice_id
            ],
            "downloadType": "AIOCD",
            "downloadFormat": "text/csv",
            "includePayment": True,

        }
        get_download_data = invoice_obj.invoice_download(workspaces_data,payload)
        InvoiceAssertion.verify_general_response_code_200(get_download_data)






