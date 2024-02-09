import io
import pandas as pd
import os
from controllers.features.order import *
from controllers.api_util.random_operations import generate_random_number
import requests

@pytest.fixture
def order(setup):
    order_res=Orders(setup)
    return order_res

class TestDownloadedFiles:

    def test_trackPoOrderFile(self,order,workspaces_data):
        payload={}
        get_track_pofile=order.get_track_po(workspaces_data,payload)
        length_file=len(get_track_pofile.json["files"])-1
        assert length_file>0,"Assertion Failure,Track po doesn't have any data"

        generate_random_file=generate_random_number(length_file)
        response_get_track_pofile=get_track_pofile.json["files"][generate_random_file]
        pofileId=get_track_pofile.json["files"][generate_random_file]["id"]


        get_download_res=order.get_download(workspaces_data,pofileId)
        data = get_download_res.text


        df = pd.read_csv(io.StringIO(data))


        excel_file_path = "trackPoDetails.xlsx"


        df.to_excel(excel_file_path, index=False)
        file_path = os.path.abspath('trackPoDetails.xlsx')

        df = pd.read_excel(r"C:\Users\91954\PycharmProjects\zono-qa-code\trackPoDetails.xlsx")

        # Convert the DataFrame to JSON
        json_data = df.to_json(orient="records")

        data = json.loads(json_data)
        logger.error(f"return the json data {json.dumps(data,indent=4)}")
        # logger.error(f"download_order_pofile{response_get_track_pofile}")
        # logger.error(f"return the length of data{len(data)}")










