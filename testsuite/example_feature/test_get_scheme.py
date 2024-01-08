
from controller.example_feature.scheme import *
import pytest
import logging


class TestProduct:
    def test_get_scheme(self,return_scheme):
        result = return_scheme.get_scheme_data
        SchemeAssertion.verify_response_code_with_201(result)

