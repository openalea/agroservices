import os
import json

credential_dir = os.path.dirname(__file__) + '/credentials/'


def get_credentials(agroservice='ipm'):
    jsonfile = credential_dir + agroservice + '.json'
    res = {}
    if os.path.exists(jsonfile):
        with open(jsonfile) as json_file:
            res = json.load(json_file)
    return res