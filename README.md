# Aixon API Auto Test

---
API Auto Test is a python based project which is triggered by Pytest.

**Install Requirements**

Please install requirements before run tests.

* pip install requirements.txt*

---

### Directory Structure
```
.
├── Jenkinsfile/ 			   # Daily Jenkins job configurations
├── config/                    # Configutations
│   ├── setup.yml     
├── controller/                    # all related model or libs
   └── example_feature/
    └── users.py
├── api_util    # All common utils
│   └── file_operations.py
│   └── db_manager.py
├── settings.py
├── testdata/                   # all test datas related to testcases
   └── example_feature/
    └── test_data.yml
├── testsuite/          		# all testcases
   └── example_feature/
    └── test_get_users.py
├── README.md
├── requirements.txt        	# Pip package requirements for execution 
└── ...
```
----

## Usage

**Step 1:** go to root of the project. (under ./example_feature folder)

**Step 2:** execute command

```
pytest -x --env=STAGING --dataset={specfic_folder}/{test_data} testsuite/{specfic_folder}/{test_suite_name}.py
```

---
````
API calls
main_url=https://api-uat.beta.pharmconnect.com
    1. send_otp : f"{self.settings.url_prefix}/sendotp"
    2. verify_otp : f"{self.settings.url_prefix}/verifyotp"
    3. workspaces : f"{self.settings.url_prefix}/workspaces"
    4. get_product : f"{self.settings.url_prefix}/commerce-v2/products/search/{principal_id}?pageNo=1&pageSize=20&customerId={invited_id}"
    5. get_scheme  : f"{self.settings.url_prefix}/commerce-v2/scheme/{principal_id}?pageNo=1&pageSize=20&skuCode=&sortDirection=&sortBy=&includeCFA=true&startDate=2023-12-05&endDate=2024-01-04&dispatchFilters=true&status=&promotionType=",
    6. get_orders  : f"{self.settings.url_prefix}/commerce-v2/orders?customerWorkspaceId={workspaces_data["clientWorkspaceId"]}&workspaceId={workspaces_data["principalWorkspaceId"]}",
    7. get_add_cart : f"{self.settings.url_prefix}/commerce-v2/orders/additemtoactiveorder/{workspaces["principalWorkspaceId"]}",
    8. get_checkout : f"{self.settings.url_prefix}/commerce-v2/orders/checkout/{workspaces["principalWorkspaceId"]}",
    9. upload_order :  f"{self.settings.url_prefix}/commerce-v2/poFile/upload/{workspaces["principalWorkspaceId"]}"
    10. upload_add_item : f"{self.settings.url_prefix}/commerce-v2/poFile/upload/{workspaces["principalWorkspaceId"]}",
    11. upload_chekcout : f"{self.settings.url_prefix}/commerce-v2/products/search/{workspaces["principalWorkspaceId"]}?customerId={workspaces["inviteId"]}&pageNo=1&pageSize=20",
```` 

#report Result 
Please install requirements before run tests
run the allure serve:allure serve reports