import re
from typing import Dict, Any

from .header import Header, BaseClass


HEADER_REGEX = re.compile("^#(.*)")
KEY_VALUE_REGEX = re.compile("(.*?):(.*)")
SETTINGS_REGEX = re.compile("^(.*):(.*)")

SETTINGS = ["set_is_list"]


class Yni(BaseClass):
    def __init__(self) -> None:
        self.variables: Dict[str, Header] = {}
        self.settings: Dict[str, bool] = {"set_is_list": False}

    @classmethod
    def from_string(cls, string: str):
        ret = {}
        settings = {}
        current_header = ret

        for line in string.splitlines():
            if line == "":
                continue

            if line.startswith("."):
                line = line.lstrip(".")

                match = SETTINGS_REGEX.search(line)
                setting, value = (match.group(1)).strip(" "), (match.group(2)).strip(" ")

                if setting not in SETTINGS:
                    raise ValueError("Setting '%s' is not a valid setting." % setting)
                if value not in ["0", "1"]:
                    raise ValueError("Setting value of '%s' is not valid." % setting)

                values = {0: False, 1: True}
                settings[setting] = values[int(value)]

            if line.startswith("#"):
                match = HEADER_REGEX.search(line)
                name = (match.group(1)).strip(" ")
                current_header = ret[name] = {}

            elif line in ["[", "]"]:
                pass

            else:
                match = KEY_VALUE_REGEX.search(line)
                key, value = match.group(1), match.group(2)
                key = key.strip("\t")
                value = value.strip(" ")
                
                if value.startswith("env("):

                    try:
                        import dotenv
                    except ImportError:
                        raise Exception("python-dotenv library is needed for env(..., ...)")

                    value = value[4:-1]
                    filename, keyname = value.split(",")
                    filename = filename.strip(" ")
                    keyname = keyname.strip(" ")

                    value = dotenv.get_key(filename, keyname)

                elif value.startswith("{"):
                    content_raw_list = [char for char in line if char not in ["{", "}"]]

                    for i, char in enumerate(content_raw_list):

                        if (char == "," and content_raw_list[i+1] == " ") or (char == ","):
                            content_raw_list[i] = "|"
                    content_raw = "".join(content_raw_list)
                    content_stripped = content_raw.replace("|", " ")
                    content_list_before = content_stripped.split(" ")
                    content_list_before.pop(0)
                    content_list = [cont for cont in content_list_before if cont]

                    value = set(content_list) if not settings["set_is_list"] else content_list

                current_header[key] = value

        yni = cls()

        for header, attributes in ret.items():
            yni.variables[header] = Header(header, attributes)
        yni.settings = settings

        return yni

    @classmethod
    def from_file(cls, filename: str):
        with open(filename, "r") as f:
            return cls.from_string(f.read())

    def __repr__(self):
        return repr(self.variables)

    def __getitem__(self, name: str):
        return self.variables[name]

    def __setitem__(self, name: str, value: Any):
        self.variables[name] = value
