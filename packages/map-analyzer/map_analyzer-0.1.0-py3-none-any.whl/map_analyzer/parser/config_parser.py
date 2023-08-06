from typing import Dict, List
from ..models import FileProperty

import toml

class ConfigParser:
    def __init__(self) -> None:
        self.compiler = ""
        self.parameters = {}            # type: Dict(str, str)
        self.file_properties = {}       # type: Dict(str, FileProperty)
        self.type_regexes = {}          # type: Dict(str, str)
        self.group_regexes = {}         # type: Dict(str, str)
        self.core_regexes = {}          # type: List(str, str)
        self.group_core_mapping = {}    # type: Dict(str, str)
        self.group_formats = {}         # type: Dict(str, str)

    def _parse_general(self, data):
        if ('compiler' in data['general']):
            self.compiler = data['general']['compiler']

    def _parse_calibration(self, data):
        param_keys = ['regex']
        for key in param_keys:
            if (key in data):
                self.parameters["calib_%s" % key] = data[key]

    def _parse_files(self, data):
        for key in data['files']:
            property = FileProperty()
            property.name = key
            property.group = data['files'][key]['group']

            self.file_properties[property.name] = property

    def _parse_type_regexes(self, data):
        for key in data['type_regexes']:
            self.type_regexes[key] = data['type_regexes'][key]

    def _parse_group_regexes(self, data):
        for key in data:
            self.group_regexes[key] = data[key]

    def _parse_group_format(self, data):
        for key in data:
            self.group_formats[key] = data[key]

    def _parse_core_regex(self, data):
        for key in data:
            self.core_regexes[key] = data[key]

    def _parse_group_core_mapping(self, data):
        for key in data:
            self.group_core_mapping[key] = data[key]

    def parse(self, name):
        data = toml.load(name)

        #print(data)
        
        if ('general' in data):
            self._parse_general(data)

        if ('calib' in data):
            self._parse_calibration(data['calib'])
        
        if ('files' in data):
            self._parse_files(data)

        if ('type_regexes' in data):
            self._parse_type_regexes(data)

        if ('group' in data):
            if ('regex' in data['group']):
                self._parse_group_regexes(data['group']['regex'])
            if ('format' in data['group']):
                self._parse_group_format(data['group']['format'])

        if ('core' in data):
            if ('regex' in data['core']):
                self._parse_core_regex(data['core']['regex'])
            if ('group' in data['core']):
                self._parse_group_core_mapping(data['core']['group'])