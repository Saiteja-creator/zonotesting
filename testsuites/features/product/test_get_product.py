
from controllers.features.product import *
import pytest
import logging


class TestProduct:
    def test_get_product(self,return_product):
        result = return_product.product_data
        ProductAssertion.verify_response_code_with_201(result)
        ProductAssertion.verify_total_product(result)
        assert result.json["products"][0]["productVariants"][0]["productVariantId"], "Assertion failure verify_productVariantId body{}".format(result.json)
        assert result.json["products"][0]["productVariants"][0]["minOrderQty"], "Assertion failure verify_qty of product body{}".format(result.json)



