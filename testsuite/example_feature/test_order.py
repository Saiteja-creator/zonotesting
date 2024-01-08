
from controller.example_feature.order import *
import pytest
import logging


class TestOrder:
    def test_get_order(self,return_orders):
        result = return_orders.get_orders_data
        OrderAssertion.verify_response_code_with_201(result)

    def test_add_cart(self,return_orders):
        result = return_orders.add_to_cart_res

        OrderAssertion.verify_response_code_with_201(result)

    def test_checkout(self,return_orders):
        result=return_orders.check_out_res
        OrderAssertion.verify_response_code_with_201(result)
