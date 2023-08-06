from __future__ import annotations

from functools import partial
import os
import re
from typing import TextIO, TypeVar

from .containers import Alert, Container, Error, Question
from .themes import Theme

T = TypeVar("T")


class PointingList:
    """
    Always points to one element in the list. The
    pointer can be moved.
    Roughly equivalent to Java's ``List`` type.
    """
    def __init__(self, it: Sequence[T]):
        self.__data = it
        self.__max_index = len(it) - 1
        self.__point_index = 0
    
    def __len__(self):
        return self.__data.__len__()
    
    def __iter__(self):
        yield from self.__data
    
    @property
    def position(self):
        return self.__point_index
    
    def get(self) -> T:
        return self.__data[self.__point_index]
    
    def point(self, index: int) -> PointingList:
        if index < 0 or index >= len(self):
            raise IndexError(f"index {index} not in range")
        
        self.__point_index = index
        return self
    
    def first(self) -> PointingList:
        self.__point_index = 0
        return self
    
    def last(self) -> PointingList:
        self.__point_index = self.__max_index
        return self
    
    def prev(self) -> PointingList:
        if self.__point_index == 0:
            self.__point_index = self.__max_index
        else:
            self.__point_index -= 1
        
        return self
    
    def next(self) -> PointingList:
        if self.__point_index == self.__max_index:
            self.__point_index = 0
        else:
            self.__point_index += 1
        
        return self

def ensure(
    expr: str,
    exc: type[BaseException] = ValueError,
) -> None:
    """
    Assert-like function taking an f-string of
    form ``f"{expr = }"`` as an argument.
    """
    m = re.match(".*= *(True|False)$", expr)
    if not m:
        raise ValueError("invalid syntax")
    
    else:
        if m.group(1) == "True":
            return
        
        else:
            raise exc(expr)

def clear_lines(amount: int) -> str:
    """
    Returns ansi escape sequence that clears the
    last ``amount`` lines.
    """
    return "\x1b[1A\x1b[2K\r" * amount

def display(
    *conts: Container,
    theme: type[Theme],
    file: TextIO,
) -> str:
    """
    Displays containers as text by styling them
    with ``theme``.
    """
    lines: list[str] = []
    cols, rows = termsize(file)
    priority = (Question, Error)
    # priority containers must come first
    
    for cont in conts:
        if cont is None:
            continue
        
        elif isinstance(cont, Alert):
            style = "\a"
        
        else:
            if not isinstance(cont, priority):
                theme._init(os.terminal_size((
                    cols,
                    rows - 1
                )))
            
            c = cont.__class__
            if c not in theme._map:
                raise RuntimeError(f"{c!r} is not mapped to any method")
            style = partial(theme._map[c], theme)(cont)
        
        if isinstance(cont, priority):
            rows -= len(style)
        
        lines.extend(style)
    
    top = "\n".join(lines)
    bottom = "\n".join(" " * cols for _ in range(rows - top.count("\n") - 1))
    return top + "\n" + bottom + "\r"

def termsize(file: TextIO) -> os.terminal_size:
    try:
        return os.get_terminal_size(file.fileno())
    except (OSError, PermissionError):
        return os.terminal_size((80, 80))
