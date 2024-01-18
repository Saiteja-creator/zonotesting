from controllers.features.scheme import *
def test_get_product(self ,return_scheme):
    result = return_scheme.get_scheme_data
    SchemeAssertion.verify_response_code_with_201(result)
    