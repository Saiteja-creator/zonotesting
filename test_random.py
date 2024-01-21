from controllers.features.order import *




# def test_pofile_checkout(setup,workspaces_data):
#     orderObj = Orders(setup)
#     order_profile = orderObj.get_pofiles(workspaces_data)
#     data_manual = []
#     for i in order_profile.json["files"]:
#         if i["importSource"] == "manual":
#             data_manual.append(i["id"])
#     orderObj.check_out(data_manual,workspaces_data)
#     update_profile = orderObj.get_pofiles(workspaces_data)
#     logger.error(f"manaul order data {json.dumps(update_profile.json,indent=4)}")