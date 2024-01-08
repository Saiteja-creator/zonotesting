
from controller.example_feature.product import *
import pytest
import logging


class TestProduct:
    def test_get_product(self,return_product):
        result = return_product.product_data
        ProductAssertion.verify_response_code_with_201(result)

