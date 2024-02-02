from controllers.features.order import *
from controllers.features.cart import *

@pytest.fixture
def cartClass(setup):
    cart=Cart(setup)
    return cart


@pytest.fixture
def get_pofile_manual_res(add_to_cart,cartClass,workspaces_data):

    get_pofile = cartClass.get_pofiles(workspaces_data)
    get_manual_last_manual = None

    for i in get_pofile.json["files"]:
        if i["importSource"] == "manual":
            get_manual_last_manual = i

    pofileId = get_manual_last_manual["id"]

    pofileLineId = []
    for i in get_manual_last_manual["lines"]:
        dict_a={}
        dict_a["orderId"] = i["orderId"]
        dict_a["orderLineId"] = i["id"]
        pofileLineId.append(dict_a)


    return [pofileId,pofileLineId]


class TestCart:

    def test_delete_by_CFA(self,get_pofile_manual_res,cartClass,workspaces_data):
        pofileId,pofileLineId = get_pofile_manual_res
        get_delete_res = cartClass.delete(pofileId,pofileLineId,workspaces_data)

        OrderAssertion.verify_response_code_with_201(get_delete_res)
        assert "Lines removed successfully" in get_delete_res.json["msg"]

        #verify, Is it remove from pofile
        get_pofile = cartClass.get_pofiles(workspaces_data)

        for i in get_pofile.json["files"]:
            assert pofileId!=i["id"],"Assertion Failure, Verify CFA delete"
    def test_single_product_delete(self,get_pofile_manual_res,cartClass,workspaces_data):
        pofileId, pofileLineId = get_pofile_manual_res
        single_pofileLineId=[pofileLineId[0]]
        get_single_delete_res=cartClass.delete(pofileId,single_pofileLineId,workspaces_data)
        OrderAssertion.verify_response_code_with_201(get_single_delete_res)


        assert "Lines removed successfully" in get_single_delete_res.json["msg"]

        #verify, Is single product delete
        get_pofile_res=cartClass.get_pofiles(workspaces_data)

        for i in get_pofile_res.json["files"]:
            if i["id"] ==pofileId:
                for j in i["lines"]:
                    assert j["id"] != single_pofileLineId,"Assertion Failure, verify single_product delete "
