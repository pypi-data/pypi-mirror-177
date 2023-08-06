from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from functools import partial
import os
from textwrap import fill, wrap #! replace this by something that handles emojis and ansi

from . import containers


def _wrap(text: str, icon: str, **kwargs) -> str:
    return wrap(
        text.replace("\n", " " * len(icon) + "\n"),
        initial_indent = icon,
        subsequent_indent = " " * len(icon),
        **kwargs,
    )

def icon(text: str) -> dict[str, str]:
    """
    Adds a symbol before text for textwrap
    calls.
    """
    return dict(
        initial_indent = text,
        subsequent_indent = " " * len(text)
    )

class Theme(ABC):
    r"""
    A theme controlls how
    :class:`containers.Container`\s are displayed.
    
    Attributes
    ----------
    _space
        Available space represented as ``os.terminal_size``.
    
    _map
        Mapping of :class:`container.Container`\s  and the
        methods that style them.
    """
    _space: os.terminal_size = None
    _textwrapper: ... = None
    
    def __new__(cls):
        cls._map = {
            containers.Error: cls.style_error,
            containers.Question: cls.style_question,
            containers.Text: cls.style_text,
            containers.Options: cls.style_options,
            containers.Confirmation: cls.style_confirmation,
            #containers.Datetime: cls.style_datetime,
            containers.Date: cls.style_date,
            containers.Integer: cls.style_integer,
        }
        return super().__new__(cls)
    
    def _init(self, space: os.terminal_size) -> None:
        self._space = space
        self._textwrapper = partial(
            _wrap,
            width = space.columns,
            replace_whitespace = False,
            drop_whitespace = False
        )
    
    @abstractmethod
    def style_error(
        self,
        content: containers.Error
    ) -> Iterable[str]: ...
    
    @abstractmethod
    def style_question(
        self,
        content: containers.Question
    ) -> Iterable[str]: ...
    
    @abstractmethod
    def style_text(
        self,
        content: containers.Text
    ) -> Iterable[str]: ...
    
    @abstractmethod
    def style_options(
        self,
        content: containers.Options
    ) -> Iterable[str]: ...
    
    @abstractmethod
    def style_confirmation(
        self,
        content: containers.Confirmation
    ) -> Iterable[str]: ...
    
    '''
    @abstractmethod
    def style_datetime(
        self,
        content: containers.Datetime
    ) -> Iterable[str]: ...
    
    @abstractmethod
    def style_date(
        self,
        content: containers.Date
    ) -> Iterable[str]: ...
    
    @abstractmethod
    def style_time(
        self,
        content: containers.Time
    ) -> Iterable[str]: ...
    '''

class Basic(Theme):
    def style_error(self, content):
        return [*self._textwrapper(
            str(content.exception),
            icon = "! "
        )]
    
    def style_question(self, content):
        return [*self._textwrapper(
            content.message,
            icon = "? ",
        ), ""]
    
    def style_text(self, content):
        return wrap(
            "*" * len(content.message) if content.hide else content.message,
            width = self._space.columns,
        )
    
    def style_option(self, content: containers.Option) -> Iterable[str]:
        return wrap(
            content.message,
            width = self._space.columns,
            initial_indent = (
                (">" if content.hover else " ")
                + ("X" if content.selected else " ")
                + " "
            )
        )
    
    def style_options(self, content):
        body: list[str] = []
        found_hover = False
        for opt in content.options:
            if not found_hover and not opt.hover:
                continue
            found_hover = True
            lines = self.style_option(opt)
            total = len(body) + len(lines)
            if total > self._space.lines:
                break
            
            body.extend(lines)
            
        return body
    
    def style_confirmation(self, content):
        return [
            "["
            + ("Y" if content.extra.get("default", False) else "y")
            + "/"
            + ("n" if content.extra.get("default", True) else "N")
            + "] "
        ]
    
    def style_date(self, content):
        return [
            f"{content.date.year} {content.date.month} {content.date.day}",
        ]
    
    def style_integer(self, content):
        return [str(content.number)]

class Circular(Theme):
    ...

class Emoji(Theme):
    ...
