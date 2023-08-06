import re

class DetailItem :
    def __init__(self) -> None:
        self.key        = ""
        self.name       = ""
        self.group      = ""
        self.core       = ""
        self.start_addr = 0
        self.size       = 0
        self.type       = ""
        self.section    = ""

    @property
    def end_addr(self) -> int:
        return self.start_addr + self.size - 1

    @property
    def long_name(self) -> str:
        if (self.group != ""):
            return "%s(%s)" % (self.group, self.name)
        return self.name

    @long_name.setter
    def long_name(self, value):
        m = re.match(r'([\w\-_.]+\.a)\(([\w\-_]+.o)\)', value)
        if (m):
            self.name  = m.group(2)
            self.group = m.group(1)
        else:
            self.name  = value
            self.group = ""

        if (self.group == ""):
            if (re.match(r'\w+Template\.o', self.name)):
                self.group = "CodeTemplate"
                self.core  = "N/A"

        m = re.match(r'^(\w+)_(src|pbconfig)\.a$',self.group)
        if (m):
            self.group = m.group(1)

        m = re.match(r"(\w+)\.(c|o)", self.name)
        if (m):
            self.key = m.group(1)
        else:
            self.key = self.name

    def __str__(self):
        lines = []
        lines.append("Name       : %s" % self.name)
        lines.append("Group      : %s" % self.group)
        lines.append("Start Addr : %x" % self.start_addr)
        lines.append("End Addr   : %x" % self.end_addr)
        lines.append("Size       : %d" % self.size)
        return "\n".join(lines)