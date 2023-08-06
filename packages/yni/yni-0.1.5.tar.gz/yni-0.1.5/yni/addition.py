from __future__ import annotations

from typing import (Any, Callable, Optional,)

DEFAULT_CHECK = lambda: ...

class Addition:
    """
    This class allows you subclass to add additions to the yni configuration file easily.
    """

    callback: Callable

    def __init__(self, line: str, executor: str, *, check: Optional[Callable[..., Any]] = None):
        self.line: str = line
        self.executor: str = executor
        
        self.user_check = check or DEFAULT_CHECK

    def check_callback(self) -> None:
        if not hasattr(self, "callback"):
            raise ValueError("No callback registered.")

    def check(self) -> None:
        self.check_callback()
        self.user_check()

    def generate_args(self) -> list[Any]:
        self.check()

        length = len(self.executor) + 1
        val = self.line[length:-1]
        commas = val.count(",")
        
        vals = val.split(",", commas)
        values: list[Any] = [val.strip(" ") for val in vals]

        return values

    def generate_kwargs(self) -> dict[Any, Any]:
        self.check()

        length = len(self.executor) + 1
        val = self.line[length:-1]
        kv: dict[Any, Any] = {}

        vals = val.split(",")

        for i, v in enumerate(vals):
            if "=" not in v.strip(" "):
                vals.pop(i)

        if "=" not in val:
            return {}

        for item in vals:
            k, v = item.split("=")
            kv[k] = v
        
        return kv

    def generate(self) -> tuple[list[Any], dict[Any, Any]]:
        args: list[Any] = self.generate_args()
        kwargs: dict[Any, Any] = self.generate_kwargs()

        res = (args, kwargs,)

        return res

    def __call__(self) -> Any:
        akw: tuple[list[Any], dict[Any, Any]] = self.generate()
        
        args, kwargs = akw

        return self.callback(args, kwargs)
