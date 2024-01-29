from controllers.features.order import *

@pytest.fixture
def test_pofile_checkout(setup,workspaces_data):
    orderObj = Orders(setup)
    order_pofile = orderObj.get_pofiles(workspaces_data)
    data_manual = []
    for i in order_pofile.json["files"]:
        if i["importSource"] == "manual":
            data_manual.append(i["id"])
    #check the previous manual order
    orderObj.check_out(data_manual,workspaces_data)
    #get pofiles data
    update_pofile = orderObj.get_pofiles(workspaces_data)

    data_clear_manual_order=[]
    for k in update_pofile.json["files"]:
        if k["importSource"] == "manual":
            data_manual.append(k["id"])
    # data_clear_manual_order should be empty

    return data_clear_manual_order


