from edge.infrastructure.config.manager import ConfigManager



class ConfigComponent:


    def __init__(self, path):

        self.config = ConfigManager(path)

        self.data = None



    def initialize(self):

        self.data = self.config.load()

        print(
            "Configuration loaded"
        )



    def get_config(self):

        return self.data



    def start(self):

        print(
            "Configuration ready"
        )



    def stop(self):

        print(
            "Configuration released"
        )