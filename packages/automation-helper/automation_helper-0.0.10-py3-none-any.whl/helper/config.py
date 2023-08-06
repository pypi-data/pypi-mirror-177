import sys
import json
from configparser import ConfigParser
from collections import namedtuple


class ConfigINI:
    def __init__(self, path_file, section):
        parser = ConfigParser()
        parser.read(path_file)
        my_dict = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                my_dict[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, path_file))
        self.data = my_dict
      
      
def _customJSONEncoder(dict_in):
    return namedtuple('X', dict_in.keys())(*dict_in.values())


class ConfigJSON:
    def __init__(self, default_json):
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        else:
            config_file = default_json
        with open(config_file, 'r') as fh:
            object_out = json.load(fh, object_hook=_customJSONEncoder)
        self.data = object_out
        self.file = config_file
