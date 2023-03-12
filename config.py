import json
import os

def cfg_item(*items):
    data = Config.instance().data
    for key in items:
        data = data[key]
    return data

class Config:
    
    __config_json_path = ["assets", "config", "config.json"]

    __instance = None
    
    @staticmethod
    def instance():
        if Config.__instance is None:
            Config()
        return Config.__instance
    
    def __init__(self):
        if Config.__instance is None:
           Config.__instance = self
           
           with open(os.path.join(*Config.__config_json_path)) as file:
               self.data = json.load(file)
        else:
            raise Exception("Config Can Only Be Instanced Once!!!") 