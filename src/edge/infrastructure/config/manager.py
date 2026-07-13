import yaml
from pathlib import Path


class ConfigManager:


    def __init__(self, path):

        self.path = Path(path)

        self.data = {}



    def load(self):

        with open(
            self.path,
            "r"
        ) as file:

            self.data = yaml.safe_load(file)


        return self.data



    def get(self, key, default=None):

        return self.data.get(
            key,
            default
        )