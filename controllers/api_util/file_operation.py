import os
import yaml
import json

def read_yml(path):
    with open(path, "r") as config:
        data = yaml.load(config, Loader=yaml.FullLoader)
    return data


def read_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data