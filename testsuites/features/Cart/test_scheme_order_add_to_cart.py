#
from controllers.features.scheme import *
from controllers.features.order import *

#

@pytest.fixture(scope="session")
def schemeClass(setup):
    return Scheme(setup)
#
@pytest.fixture(scope="session")
def orderClass(setup):
    return Orders(setup)

@pytest.fixture
def single_product_scheme_add_to_cart(test_pofile_checkout,return_product,orderClass,workspaces_data):
    #product response from conftest data
    product_Data_res = return_product.product_data
    OrderAssertion.verify_response_code_with_201(product_Data_res)

    data_list = []
    get_single_scheme_product = False
    data_scheme_product=[]
    for i in product_Data_res.json["products"]:
        for j in i["productVariants"]:
            if len(j["promotions"]) > 0:
                data_scheme_product=j
                scheme_code=j["promotions"][0]["id"]
                data_list.append(
                    {"productVariantId": j["productVariantId"], "quantity": j["minOrderQty"], "operator": "add"})
                min_order_qty=j["minOrderQty"]
                get_single_scheme_product = True
        if get_single_scheme_product:
            break




    #get_add_to_cart_res = orderClass.Cart(workspaces_data,data_list,source)

    return [data_scheme_product,data_list]





class TestSchemeProduct:
    def test_add_to_cart(self,single_product_scheme_add_to_cart,orderClass,workspaces_data):
        data_scheme_product, data_list=single_product_scheme_add_to_cart
        source="manual"
        add_cart_res=orderClass.add_to_cart(workspaces_data,data_list,source)
        #verify Cart
        OrderAssertion.verify_response_code_with_201(add_cart_res)

        get_pofile_res=orderClass.get_pofiles(workspaces_data)


        product_pofile_res=get_pofile_res.json["files"][-1]["lines"][-1]
        OrderAssertion.verify_general_response_code_200(get_pofile_res)

        #verify mode
        assert product_pofile_res["modeOfOrder"] == "manual"

        #verify data_product_scheme and get_pofile_res
        assert data_scheme_product["productVariantId"] == product_pofile_res["productVariantId"]

        #verify data_product_scheme and get_pofile_res qty
        assert product_pofile_res["quantity"]%data_scheme_product["minOrderQty"] == 0


        #verify saving
        saving_cal_pofile = round(
            (product_pofile_res["linePriceWithTax"] - product_pofile_res["discountedLinePriceWithTax"]), 2)

        assert  saving_cal_pofile == float(add_cart_res.json["orders"][0]["orderLine"][-1]["adjustments"][0]["lineDiscount"])

        #
        #assert float(add_cart_res.json["orders"][0]["orderLine"][-1]["adjustments"][0]["lineDiscount"]) > 0
        #logger.error(f"return the data_scheme{data_scheme_product}")
        #logger.error(f"return the product pofile_res{product_pofile_res}")






    def test_scheme(self,workspaces_data,single_product_scheme_add_to_cart,schemeClass):
        data_scheme_product, data_list = single_product_scheme_add_to_cart

        scheme_code = data_scheme_product["promotions"][0]["id"]
        get_scheme_code_res=schemeClass.get_scheme_code(scheme_code,workspaces_data)

        #verifySchemeCode
        assert get_scheme_code_res.json["id"] == scheme_code, "Assertion Failure, Verify Scheme_code from get_scheme_code_res"

        #verify ProductVariant
        assert data_scheme_product["productVariantId"] == int(get_scheme_code_res.json['productVariantIds'][2:-2]),"Assertion Failure, verify get_product_scheme_product_res and scheme_code_res"

        #verify_minimumQty
        assert get_scheme_code_res.json["minimumQty"]== data_scheme_product["minOrderQty"],"Assertion Failure, verify scheme_code_response and product_scheme_response"

        #verify ptr
        assert get_scheme_code_res.json["ptr"] == data_scheme_product["PTR"],"Assertion Failure, verify PTR"




