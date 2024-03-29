from controllers.features.scheme import *


@pytest.fixture(scope="module")
def schemeClass(setup):
    return Scheme(setup)


class TestSchemePage:

    def test_pts_asc_res(self,workspaces_data,schemeClass):
        filter_data = {
            "sortDirection": "ASC",
            "sortBy": "ProductPrice"
        }
        filter_pts_ASC= schemeClass.get_scheme_filter(workspaces_data, filter_data)

        SchemeAssertion.verify_response_code_with_201(filter_pts_ASC)
        for i in range(len(filter_pts_ASC.json["promotions"])-1):
            present_pts_value=filter_pts_ASC.json["promotions"][i]["pts"]
            next_pts_value=filter_pts_ASC.json["promotions"][i+1]["pts"]

            assert next_pts_value>=present_pts_value, "Assertion Failure,Verify filter of pts_asc"


    def test_pts_desc_res(self,workspaces_data,schemeClass):
        filter_data = {
            "sortDirection": "DESC",
            "sortBy": "ProductPrice"
        }

        filter_pts_desc=schemeClass.get_scheme_filter(workspaces_data,filter_data)

        SchemeAssertion.verify_response_code_with_201(filter_pts_desc)

        for i in range(len(filter_pts_desc.json["promotions"])-1):
            present_pts_value=filter_pts_desc.json["promotions"][i]["pts"]
            next_pts_value=filter_pts_desc.json["promotions"][i+1]["pts"]

            assert next_pts_value<=present_pts_value, "Assertion Failure,Verify filter of pts_DESC"


    def test_pageNo_change(self,schemeClass,workspaces_data):
        filter_data = {
            "pageNo": 2,
        }

        filter_pageNo = schemeClass.get_scheme_filter(workspaces_data, filter_data)
        SchemeAssertion.verify_response_code_with_201(filter_pageNo)
        assert filter_pageNo.json["startRecord"] != 1, "Assertion Failure, Verify pageNO"

    def test_pageSize_change(self,schemeClass,workspaces_data):
        #get_scheme_data and verify length of scheme,After apply the pageSizevalue
        pageSizeValue=30
        filter_data = {
            "pageNo": 1,
            "pageSize": pageSizeValue,
            "dispatchFilters": True,
            # "skuCode":"",
            # "sortDirection":"",
            # "sortBy":"",
            # "startDate":"2024-01-02",
            # "endDate":"2024-02-01"

        }

        filter_pageSize=schemeClass.get_scheme_filter(workspaces_data,filter_data)
        SchemeAssertion.verify_response_code_with_201(filter_pageSize)


        total_records_pageSize=filter_pageSize.json["endRecord"]-filter_pageSize.json["startRecord"]+1
        assert total_records_pageSize <= pageSizeValue, "Assertion Failure, Verify PageSize"



