from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
import datetime as dt
from typing import Any, Optional


@dataclass
class Final:
    """
    A dataclass denoting the result of a prompt
    function. The purpose of yielding this instead
    of returning is that in case of a failed validation
    the prompt should still be iterable.
    """
    content: Any

@dataclass
class Object:
    instance_of: Container
    lines: Iterable[str]

@dataclass
class Container:
    extra: dict[str, Any] = field(kw_only = True, default_factory = dict)

@dataclass
class Alert(Container):
    pass

@dataclass
class Error(Container):
   exception: BaseException

@dataclass
class Integer(Container):
    number: int

@dataclass
class Text(Container):
    message: str
    hide: bool = False

@dataclass
class Confirmation(Container):
    pass

@dataclass
class Option(Container):
    message: str
    selected: Optional[bool] = None
    hover: Optional[bool] = None

@dataclass
class Options(Container):
    options: Iterable[Options] = field(default_factory = list)

@dataclass
class Question(Container):
    message: str

@dataclass
class Datetime(Container):
    datetime: dt.datetime

@dataclass
class Date(Container):
    date: dt.date

@dataclass
class Time(Container):
    time: dt.time
