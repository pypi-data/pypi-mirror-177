from abc import ABCMeta
from typing import Dict, List
from ..models import DetailItem, DetailGroup, FileProperty, CoreGroup

import re

class MapParser(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.lines = []
        self.items = []    # type: List[DetailItem]
        self.cores = {}    # type: Dict[str, DetailGroup]

    def parse(self, file_name, parameters: Dict[str, str]) -> None:
        pass

    def display_items(self):
        for value in self.items.values():
            print(value)

    def display_lines(self):
        for line in self.lines:
            print(line)

    def display_groups(self):
        for value in self.groups.values():
            print(value)

    def display(self) -> None:
        self.display_lines()
        self.display_items()

    def patch_value_with_regex(self, value):
        m = re.match("\$(\d)", value)
        if (m):
            return ("int", int(m.group(1)))
        else:
            return ("str", value)

    def patch_file_property(self, file_properties: Dict[str, FileProperty]):
        print("Patch file property")

        for item in self.items:
            if item.key in file_properties:
                item.group = file_properties[item.key].group

    def patch_type(self, type_regexes: Dict[str, str]):
        print("Patch type")

        for item in self.items:
            for type_regex in type_regexes:
                m = re.match(type_regex, item.type)
                if (m):
                    item.type = type_regexes[type_regex]

    def patch_group(self, group_regexes: Dict[str, str]):
        print("Patch group")

        for item in self.items:
            for regex in group_regexes:
                m = re.match(regex, item.name, re.IGNORECASE)
                if (m):
                    (type, value) = self.patch_value_with_regex(group_regexes[regex])
                    if (type == "int"):
                        item.group = m.group(value)
                    else:
                        item.group = value

    def format_group_name(self, group_formats: Dict[str, str]):
        print("Format group name")

        for item in self.items:
            for regex in group_formats:
                m = re.match(regex, item.group, re.IGNORECASE)
                if (m):
                    (type, value) = self.patch_value_with_regex(group_formats[regex])
                    if (type == "int"):
                        item.group = m.group(value)
                    else:
                        item.group = value

    def patch_core(self, core_regexes: Dict[str, str]):
        print("Patch core by file name")

        for item in self.items:
            for regex in core_regexes:
                m = re.match(regex, item.name, re.IGNORECASE)
                if (m):
                    (type, value) = self.patch_value_with_regex(core_regexes[regex])
                    if (type == "int"):
                        item.core = "Core %s" % m.group(value)
                    else:
                        item.core = value

    def patch_group_core_mapping(self, mapping: Dict[str, str]):
        print("Patch core by group name")
        
        for item in self.items:
            if item.group in mapping:
                item.core = mapping[item.group]

    def get_core_instance(self, core_name):
        if (core_name == ""):
            core_name = "Unknown"

        if (core_name not in self.cores):
            core = CoreGroup()
            core.name = core_name
            self.cores[core_name] = core
        return self.cores[core_name]

    def get_group_instance(self, core: CoreGroup, group_name):
        if (group_name == ""):
            group_name = "misc"

        if group_name not in core.groups:
            group = DetailGroup()
            group.name = group_name
            core.groups[group_name] = group

        return core.groups[group_name]

    def analyze_core_data(self):
        print("Summarize data ...")
        for item in self.items:
            core = self.get_core_instance(item.core)
            group = self.get_group_instance(core, item.group)

            group.items.add(item.name)

            if item.type == "text" or item.type == ".mk_text":
                group.text_total += item.size
            elif item.type == "bss":
                group.bss_total += item.size
            elif item.type == "rodata" or item.type == ".mk_exceptiontable":
                group.rodata_total += item.size
            elif item.type == "data":
                group.data_total += item.size
            elif item.type == "calibration":
                group.calib_total += item.size
            elif item.type == ".mk_corelocaldata":
                pass
            else:
                raise ValueError("Invalid type <%s> is not supported" % item.type)
        
