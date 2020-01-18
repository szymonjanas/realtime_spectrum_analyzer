import json

class Config:
    def __init__(self):
        self.data = None
        with open('c:/Users/szymo/OneDrive/Documents/music_visualisation/rt_spectrum_analyzer/config.json') as json_data_file:
            self.data = json.load(json_data_file)

    def get_settings(self, arg: str):
        return self.data[arg]
