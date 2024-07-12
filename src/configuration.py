## @file configuration.py
#  @author Jack Duignan (JackpDuignan@gmail.com)
#  @date 2024-06-06
#  @brief A custom configuration reader file to simplify reading json files
#
#  @cite https://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file

import json
from typing import Union

class ConfigDict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def save_json(self, path):
        filename = path

        with open(filename, "w+") as f:
            json.dump(self, f, indent=4)
            f.close()

class Config(object):
    @staticmethod
    def __load__(data):
        if type(data) is dict:
            return Config.load_dict(data)
        elif type(data) is list:
            return Config.load_list(data)
        else:
            return data

    @staticmethod
    def load_dict(data: dict):
        result = ConfigDict()
        for key, value in data.items():
            result[key] = Config.__load__(value)
        return result

    @staticmethod
    def load_list(data: list):
        result = [Config.__load__(item) for item in data]
        return result

    @staticmethod
    def load_json(path: str) -> Union[ConfigDict, list]:
        with open(path, "r") as f:
            result = Config.__load__(json.loads(f.read()))
        return result
    
def test(config):
    config.version = 2


if __name__ == "__main__":
    with open("test.json", "w+") as f:
        f.writelines(["{\n", "    \"version\": 1,\n", "    \"display\": true\n", "}\n"])
        f.close()

    loaded_config = Config.load_json("test.json")
    loaded_config.version = 3

    loaded_config.save_json("test.json")
