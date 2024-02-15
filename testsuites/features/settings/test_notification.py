
from controllers.features.Settings.setting import *
from controllers.api_util.random_operations import *
@pytest.fixture
def setting_obj(setup):
    settings=SettingCls(setup)
    return settings


notification_list = ["isEmail", "isSms", "isWeb", "isNative"]




class TestSettings:
    def test_get_notification_res(self,setting_obj,workspaces_data):
        notification_res=setting_obj.get_notification_res(workspaces_data)
        SettingAssertions.verify_general_response_code_200(notification_res)

        assert notification_res.json["NotificationPreferences"],"Assertion Failure, NotificationPreferences"
        assert notification_res.json["partyType"] == "BUYER", "Assertion Failure, Verify partyType status"
        notification_preferences_res=notification_res.json["NotificationPreferences"][0]
        assert "appId" in notification_preferences_res, "Assertion Failure, Verify appId res from Notification"
        list_filed_notification = ["isEmail", "isSms", "isWeb", "isNative"]
        for i in list_filed_notification:
            assert i in notification_preferences_res,f"Assertion Failure, Verify each key in notification_response:{i}"

    @pytest.mark.parametrize("each_params",notification_list)
    def test_onClick_notification(self,each_params,setting_obj,workspaces_data):
        notification_res = setting_obj.get_notification_res(workspaces_data)
        SettingAssertions.verify_general_response_code_200(notification_res)
        length=len(notification_res.json["NotificationPreferences"])-1
        random_num = generate_random_number(length)
        previous_response = notification_res.json["NotificationPreferences"][random_num][each_params]


        update_value=not previous_response

        notificationPreferences_dict = {}
        notificationPreferences_dict["appId"] = notification_res.json["NotificationPreferences"][random_num]["appId"]
        notificationPreferences_dict["partyType"] = "BUYER"
        notificationPreferences_dict[each_params] = update_value

        payload = {
            "NotificationPreferences": [notificationPreferences_dict]
        }


        update_notification=setting_obj.update_notification_res(workspaces_data,payload)

        SettingAssertions.verify_response_code_with_201(update_notification)
        get_notification_res = setting_obj.get_notification_res(workspaces_data)
        update_notification_response = get_notification_res.json["NotificationPreferences"][random_num][each_params]


        for each_key in notification_res.json["NotificationPreferences"][random_num]:
            if each_key == each_params:
                assert get_notification_res.json["NotificationPreferences"][random_num][each_key] != notification_res.json["NotificationPreferences"][random_num][each_key] , f"Assertion Failure, Verify the notification update: {each_params}"
            else:
                assert get_notification_res.json["NotificationPreferences"][random_num][each_key] == notification_res.json["NotificationPreferences"][random_num][each_key], f"Assertion Failure, Verify the notification of other fileds : {each_params}"






























