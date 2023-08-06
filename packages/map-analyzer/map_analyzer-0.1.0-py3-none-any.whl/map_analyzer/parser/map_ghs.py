from .map import MapParser
from ..models import DetailItem
from typing import Dict

import re

class GhsMapParser(MapParser):
    def __init__(self) -> None:
        super().__init__()

    def _parse_item(self, line) -> None:
        m = re.match(r'([0-9a-f]+)\+([0-9a-f]+)\s+([\w.]+)\s+->\s+(\w+)\s+([\w\-.()]+)', line)
        if (m):
            item = DetailItem()
            item.long_name  = m.group(5)
            item.start_addr = int(m.group(1), base=16)
            item.size       = int(m.group(2), base=16)
            item.type       = m.group(3)
            item.section    = m.group(4)
            
            self.items.append(item)

    def _parse_calibration_item(self, line, regex):
        m = re.match(regex, line)
        if (m):
            item = DetailItem()
            item.long_name  = m.group(4)
            item.start_addr = int(m.group(1), base=16)
            item.size       = int(m.group(2), base=16)
            item.type       = "calibration"
            item.section    = m.group(3)

            self.items.append(item)
    
    def parse(self, file_name, params: Dict[str, str]) -> None:
        print("Start to parse %s..." % file_name)

        with open(file_name) as f_in:
             for line in f_in:
                m = re.match(r'([0-9a-f]+)\+([0-9a-f]+)\s+[\w.]+\s+->\s+(\w+)\s+([\w\-.()]+)', line)
                if (m):
                    self.lines.append(m.group(0))
                    self._parse_item(line)
                
                if ('calib_regex' in params):
                    m = re.match(params['calib_regex'], line)
                    if (m):
                        self.lines.append(m.group(0))
                        self._parse_calibration_item(line, params['calib_regex'])
                        
