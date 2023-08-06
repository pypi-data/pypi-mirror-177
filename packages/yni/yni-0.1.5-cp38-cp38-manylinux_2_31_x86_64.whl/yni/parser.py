from __future__ import annotations

import re
from typing import Dict, Any, List, Optional, Callable

from .header import Header, BaseClass

from .addition import Addition


HEADER_REGEX = re.compile("^#(.*)")
KEY_VALUE_REGEX = re.compile("(.*?):(.*)")
SETTINGS_REGEX = re.compile("^(.*):(.*)")

SETTINGS = ["set_is_list"]

class Env(Addition):
    """
    Environment addition.
    """

    def __init__(self, line: str, executor: str, *, check: Optional[Callable[..., Any]] = None):
        
        def ucheck():
            try:
                import dotenv
            except (ImportError, ModuleNotFoundError):
                raise Exception("python-dotenv library is needed for env(..., ...)")

        super().__init__(line, executor, check=ucheck)

    def callback(self, args: list[str], kwargs: dict[str, str]) -> Any:
        import dotenv

        filename, keyname = args

        return dotenv.get_key(filename, keyname)

class Yni(BaseClass):
    def __init__(self) -> None:
        self.variables: Dict[str, Header] = {}
        self.settings: Dict[str, bool] = {"set_is_list": False}
        self.additions: Dict[str, tuple[type[Addition], Optional[Callable[..., Any]]]] = {"env": (Env, None)}

    @classmethod
    def from_string(cls, string: str):
        ret: dict = {}
        settings = {}
        yni = cls()
        current_header = ret

        for line in string.splitlines():
            if line == "":
                continue

            if line.startswith("."):
                line = line.lstrip(".")

                match = SETTINGS_REGEX.search(line) # type: ignore
                setting, value = (match.group(1)).strip(" "), (match.group(2)).strip(" ") # type: ignore

                if setting not in SETTINGS:
                    raise ValueError("Setting '%s' is not a valid setting." % setting)
                if value not in ["0", "1"]:
                    raise ValueError("Setting value of '%s' is not valid." % setting)

                values = {0: False, 1: True}
                settings[setting] = values[int(value)]

            if line.startswith("#"):
                match = HEADER_REGEX.search(line)
                name = (match.group(1)).strip(" ") # type: ignore
                current_header = ret[name] = {}

            elif line in ["[", "]"]:
                pass

            else:
                match = KEY_VALUE_REGEX.search(line)
                key, value = match.group(1), match.group(2) # type: ignore
                key = key.strip("\t")
                value = value.strip(" ")
                
                for k, a in zip(yni.additions.keys(), yni.additions.values()):
                    if value.startswith(f"{k}("):
                        value = yni.call_addition((a[0])(value, k, check=a[1]))

                else:
                    if value.startswith("{"):
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

        for header, attributes in ret.items():
            yni.variables[header] = Header(header, attributes)
        yni.settings = settings

        return yni

    def call_addition(self, addition: Addition) -> Any:
        a = addition()

        return a

    def add_addition(self, executor: str, addition: type[Addition], *, check: Optional[Callable[..., Any]] = None) -> Any:
        self.additions[executor] = (addition, check)

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
