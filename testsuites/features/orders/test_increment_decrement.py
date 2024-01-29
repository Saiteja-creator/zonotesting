# import logging

from controllers.features.order import *
#
@pytest.fixture(scope="session")
def orderClass(setup):
    return Orders(setup)

# def test_increment(return_scheme,workspaces_data,orderClass):
#     add_to_cart_res=test_get_scheme_add_to_card(return_scheme,workspaces_data,orderClass)
#     pofile_id=add_to_cart_res.json["orders"][0]["pofileId"]
#     pofileLineId=add_to_cart_res.json["orders"][0]["orderLine"][-1]["id"]
#     workspaces, product_data, source_data
#     orderClass.add_to_cart(workspaces_data,)
#     print(pofile_id)


# def test_increment(test_get_scheme_add_to_card,return_scheme,workspaces_data,orderClass):
#     get_scheme_data=return_scheme.get_scheme_data
#     scheme_list = []
#     for i in get_scheme_data.json["promotions"]:
#         productVar = int(i["productVariantIds"][2:-2])
#         scheme_list.append({"productVariantId": productVar, "quantity": i["minimumQty"], "operator": "add"})
#         break
#
#     source = "manual"
#     get_add_to_cart = orderClass.add_to_cart(workspaces_data, scheme_list, source)
#     print(f"return the data{test_get_scheme_add_to_card.json}")
#

