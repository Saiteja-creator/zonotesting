import yaml
from enum import Enum
from controllers.api_util.file_operation import read_yml

class TestsuiteSettings:
    def __init__(self):
        self.url_prefix = ""
        self.api_version = Settings.DEFAULT_API_VERSION

class EnumTestEnvironment(str,Enum):
    STAGING = "STAGING"
    PROD = "PRODUCTION"

class Settings:
    DEFAULT_API_VERSION = "v1"
    DEFAULT_SETTING_CONFIG = "./config/setup.yml"

    def _init_variables(self):

        self.url_prefix = self.setup_config[self.environment]["URL_PREFIX"]

    def __init__(self,request):
        args={
            "env" : request.config.getoption("--env",default=None),
            "dataset" : request.config.getoption("--dataset",default=None),
            "api-version" : request.config.getoption("--api_version",default=None),
            "setting_file" : request.config.getoption("--setting_file",default=None)
        }
        self.set_env(args['env'])
        self.dataset = self.set_dataset(args["dataset"])
        self.api_version = args["api-version"] if args["api-version"] else Settings.DEFAULT_API_VERSION
        if args["setting_file"]:
            self.DEFAULT_SETTING_CONFIG = args["setting_file"]

        with open(self.DEFAULT_SETTING_CONFIG,"r") as config:
            self.setup_config = yaml.load(config,Loader=yaml.FullLoader)

            self._init_variables()
    def set_env(self,env:str):
        if env is not None:
            self.environment=env.upper()
        else:

            self.environment= str(self.setup_config["Environment"]).upper()

        for enum_env in EnumTestEnvironment:
            if self.environment ==  enum_env.value:
                self.environment=enum_env
                break
        if not self.environment:
            self.environment=EnumTestEnvironment.STAGING

    def set_dataset(self,data_name:str):
        data = read_yml(f'./testdata/{data_name}.yml')
        return data



