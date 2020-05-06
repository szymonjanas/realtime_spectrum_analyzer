import json
import os

data = None
with open("config.json") as json_data_file:
    data = json.load(json_data_file)

def get_settings(arg: str):
    return data[arg]
