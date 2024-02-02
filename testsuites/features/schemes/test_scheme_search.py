from controllers.features.scheme import *
from controllers.features.random_operations import generate_random_number


@pytest.fixture(scope="module")
def schemeClass(setup):
    return Scheme(setup)


class TestSchemeSearch:

    def test_scheme_search_sku(self,workspaces_data,schemeClass,return_scheme):
        promotions=return_scheme.get_scheme_data.json["promotions"]
        length=len(promotions)

        generate_random_number_res=generate_random_number(length-1)
        search_key_res=promotions[generate_random_number_res]["sku"][0][:4]

        filter_data = {
            "searchKey": search_key_res
        }
        get_scheme_id=schemeClass.get_scheme_filter(workspaces_data,filter_data)
        SchemeAssertion.verify_response_code_with_201(get_scheme_id)
        #check each_scheme sku no

        for i in get_scheme_id.json["promotions"]:
            assert search_key_res in i["sku"][0] or search_key_res in i["title"],"assertion failure,verify search key sku code"


    def test_scheme_search_sku_manual(self, workspaces_data, schemeClass, return_scheme):
        promotions = return_scheme.get_scheme_data.json["promotions"]
        length = len(promotions)

        generate_random_number_res = generate_random_number(length - 1)
        search_key_res = 22222

        filter_data = {
            "searchKey": search_key_res
        }
        get_scheme_id = schemeClass.get_scheme_filter(workspaces_data, filter_data)
        SchemeAssertion.verify_response_code_with_201(get_scheme_id)

        assert get_scheme_id.json["totalRecords"] == 0




        # check each_scheme sku no

        # for i in get_scheme_id.json["promotions"]:
        #     assert search_key_res in i["sku"][0] or search_key_res in i["title"]



    def test_scheme_title(self,return_scheme,schemeClass,workspaces_data):
        promotions = return_scheme.get_scheme_data.json["promotions"]
        length = len(promotions)

        generate_random_number_res = generate_random_number(length-1)
        search_key_res_title = promotions[generate_random_number_res]["title"]
        half_length = (len(search_key_res_title))//2
        search_key_half_length=search_key_res_title[:half_length]

        filter_data = {
            "searchKey": search_key_half_length
        }

        get_scheme_title_res = schemeClass.get_scheme_filter(workspaces_data, filter_data)
        SchemeAssertion.verify_response_code_with_201(get_scheme_title_res )

        for i in get_scheme_title_res .json["promotions"]:
            assert search_key_half_length in i["title"],"Assertion Failure, verify scheme search key title"


    def test_scheme_title_manual(self,return_scheme,schemeClass,workspaces_data):
        promotions = return_scheme.get_scheme_data.json["promotions"]
        length = len(promotions)

        generate_random_number_res = generate_random_number(length-1)

        search_key="Saiteja"

        filter_data = {
            "searchKey": search_key
        }

        get_scheme_title_res = schemeClass.get_scheme_filter(workspaces_data, filter_data)
        SchemeAssertion.verify_response_code_with_201(get_scheme_title_res)

        for i in get_scheme_title_res .json["promotions"]:
            assert search_key in i["title"],"Assertion Failure, verify scheme search key title"

