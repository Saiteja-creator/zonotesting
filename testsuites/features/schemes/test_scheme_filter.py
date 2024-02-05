from controllers.features.scheme import *
from controllers.api_util.random_operations import generate_random_number


@pytest.fixture(scope="module")
def schemeClass(setup):
    return Scheme(setup)




class TestSchemeFilter:

    def test_get_test_scheme(self,return_scheme,workspaces_data,schemeClass):
        get_filter_scheme=return_scheme.get_scheme_data
        for i in get_filter_scheme.json["promotions"]:
            assert i["promotionType"] == "product_discount","Assertion failure,verify get_scheme"
            assert i["id"]


   #filter filed
    def test_single_division_id(self,return_scheme,workspaces_data,schemeClass):
        scheme_res=return_scheme.get_scheme_data.json
        length=len(scheme_res["division"])
        generate_random_no = generate_random_number(length-1)
        division_id=scheme_res["division"][generate_random_no]["divisionId"]

        filter_data={}

        payload={"divisionFilter":[division_id]}
        get_scheme_filter_res=schemeClass.get_scheme_filter(workspaces_data, filter_data,payload)

        SchemeAssertion.verify_response_code_with_201(get_scheme_filter_res)
        res_div=False
        for i in get_scheme_filter_res.json["division"]:
            if i["divisionId"] == division_id:
                res_div=True
        # pending assert for divisionId verification

    # filter filed
    def test_multiple_filter_divisionsIds(self,return_scheme,schemeClass,workspaces_data):

        scheme_res = return_scheme.get_scheme_data.json
        length=len(scheme_res["division"])//2
        division_ids=[]
        for i in range(length):
            each_division_id=scheme_res["division"][i]["divisionId"]
            division_ids.append(each_division_id)

        filter_data = {}

        payload = {"divisionFilter": division_ids}
        get_scheme_multiple_divisions=schemeClass.get_scheme_filter(workspaces_data, filter_data,payload)
        SchemeAssertion.verify_response_code_with_201(get_scheme_multiple_divisions)
        #pending assert for divisionIds verification




    # filter scheme_sku full
    def test_sku_filter_scheme(self,return_scheme,workspaces_data,schemeClass):
        promotions = return_scheme.get_scheme_data.json["promotions"]
        length = len(promotions)

        generate_random_number_res = generate_random_number(length - 1)
        search_key_res = promotions[generate_random_number_res]["sku"][0]

        filter_data = {
            "skuCode": search_key_res
        }
        get_scheme_id = schemeClass.get_scheme_filter(workspaces_data, filter_data)
        SchemeAssertion.verify_response_code_with_201(get_scheme_id)
        assert get_scheme_id.json["totalRecords"] == 1

        # check each_scheme sku no
        for i in get_scheme_id.json["promotions"]:
            assert i["sku"][0] == search_key_res,"Assertion failure,filter scheme sku code"


    def test_sku_filter_scheme_manual(self,return_scheme,workspaces_data,schemeClass):
        filter_data = {
            "skuCode": "0000"
        }
        get_scheme_id = schemeClass.get_scheme_filter(workspaces_data, filter_data)
        SchemeAssertion.verify_response_code_with_201(get_scheme_id)
        assert get_scheme_id.json["totalRecords"] == 0,"Assertion Failure,Verify scheme sku code manual"

   #scheme filter offer & free_products

    def test_scheme_filter_offer(self,schemeClass,workspaces_data):

        filter_data = {
            "promotionType": "product_discount"
        }
        get_scheme_filter_offer = schemeClass.get_scheme_filter(workspaces_data, filter_data)



        for i in get_scheme_filter_offer.json["promotions"]:

            assert i["promotionType"] == "product_discount","Assertion Failure,Verify scheme offer"

    def test_scheme_filter_free_product(self,schemeClass,workspaces_data):
        filter_data = {
            "promotionType": "buy_x_get_y_free"
        }
        get_scheme_filter_free_product = schemeClass.get_scheme_filter(workspaces_data, filter_data)



        for i in get_scheme_filter_free_product.json["promotions"]:
            assert i["promotionType"] == "buy_x_get_y_free","Assertion Failure, Verify scheme free_product"


    def test_clear_filter(self,return_scheme,schemeClass,workspaces_data):
        promotions = return_scheme.get_scheme_data.json["totalRecords"]

        filter_data = {
            "promotionType": "buy_x_get_y_free"
        }
        get_scheme_filter_free_product = schemeClass.get_scheme_filter(workspaces_data, filter_data)

        filter_update_data = {
            "dispatchFilters": "true"
        }

        get_clear_filter = schemeClass.get_scheme_filter(workspaces_data,filter_update_data)

        SchemeAssertion.verify_response_code_with_201(get_clear_filter)
        assert get_clear_filter.json["totalRecords"] == promotions,"Assertion Failure, Verify scheme clear filter"





