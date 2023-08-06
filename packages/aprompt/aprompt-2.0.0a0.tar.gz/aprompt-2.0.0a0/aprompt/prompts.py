# TODO: add H, J, K, L for navigation
# TODO: add navigation info
# TODO: fix PAGE_UP and PAGE_DOWN keys
# TODO: make container import cleaner
# TODO: containers.Final[T]

from __future__ import annotations

from collections.abc import Generator
import datetime as dt
from typing import Optional, overload, TypeVar

from readchar import key as keys

from .containers import (
    Alert,
    Confirmation,
    Container,
    Date,
    Final,
    Integer,
    Option,
    Options,
    Text,
)
from ._utils import ensure, PointingList


T = TypeVar("T")
PromptFunction = Generator[list[Container], str, None]


def confirm(
    *,
    default: bool = True,
) -> PromptFunction[bool]:
    """
    Prompts for confirmation
    
    Parameters
    ----------
    default
        This is returned when no character was
        entered.
    """
    alert = False
    while True:
        key = yield [
            Alert() if alert else None,
            Confirmation(
                extra = dict(
                    default = default
                )
            )
        ]
        alert = False
        
        if key in "yY":
            yield Final(True)
        
        elif key in "nN":
            yield Final(False)
        
        elif key == keys.ENTER:
            yield Final(default)
        
        else:
            alert = True

def number(
    *,
    mn: Optional[int] = None,
    mx: Optional[int] = None,
    default: Optional[int] = None,
    step: int = 1,
) -> PromptFunction[int]:
    """
    Parameters
    ----------
    mn
        Optional minimum number. Must be less than
        or equal to ``default``.
    
    mx
        Optional maximum number. Must be greater than
        or equal to ``default``.
    
    default
        The number to begin from. Defaults to ``mn``
        if specified, otherwise ``0`` or ``mx`` if ``mx < 0``.
    
    step
        Increases/decreases the number by this value
        each time. When the number reaches a value
        greater than ``mx`` or less than ``mn``, it
        will turn into one of these respectively.
        
    """
    if default is None:
        if mn is not None and mx is not None:
            ensure(f"{mn <= mx}")
        default = mn if mn is not None else mx if mx is not None and mx <= 0 else 0
    
    else:
        if mn is not None:
            ensure(f"{mn <= default}")
        
        if mx is not None:
            ensure(f"{mx >= default}")
    
    value = default
    step = abs(step)
    
    alert = False
    while True:
        key = yield [
            Alert() if alert else None,
            Integer(number = value)
        ]
        alert = False
        
        if key == keys.ENTER:
            yield Final(value)
        
        elif key == keys.UP:
            value += step
            if mx is not None and value > mx:
                value = mx
        
        elif key == keys.DOWN:
            value -= step
            if mn is not None and value < mn:
                value = mn
        
        else:
            alert = True

def text(
    *,
    hide: bool = False,
    default: str = "",
    placeholder: Optional[str] = None,
) -> PromptFunction[str]:
    """
    Prompts a text.
    
    Parameters
    ----------
    hide
        Hides the entered characters from the
        user. The appearance depends on the
        theme.
    
    default
        This is returned when no characters were
        entered.
    
    placeholder
        Text that is displayed in a different
        shade to give the user an idea of what
        is expected.
    
    Returns
    -------
    The entered text.
    """
    display = ""
    while True:
        key = yield [Text(
            display,
            hide = hide,
            extra = dict(
                default = default,
                placeholder = placeholder
            ),
        )]
        
        if key == keys.ENTER:
            yield Final(display or default)
        
        display += key

@overload
def choice(multiple: Literal[True]) -> PromptFunction[list[str]]: ...

@overload
def choice(multiple: Literal[False]) -> PromptFunction[str]: ...

def choice(
    *options: str,
    multiple: bool = False,
    sort: bool = False,
):
    """
    Parameters
    ----------
    options
        All options to choose from.
    
    multiple
        Enables multiple selection.
    
    sort
        Sort the options by using :pyfn:`sorted`.
    """
    if sort:
        options = sorted(options)
    
    opts = Options(options = PointingList(list(Option(
        message = o,
        selected = False,
        hover = not bool(i) # first is True, then all False
    ) for i, o in enumerate(options))))
    
    alert = False
    while True:
        key = yield [
            Alert() if alert else None,
            opts
        ]
        alert = False
        
        if key == keys.ENTER:
            if multiple:
                yield Final([o.message for o in opts.options if o.selected])
            
            yield Final(opts.options.get().message)
        
        elif key == " " and multiple:
            opts.options.get().selected = not opts.options.get().selected
        
        elif key == keys.UP:
            opts.options.get().hover = False
            now = opts.options.prev()
            now.get().hover = True
            opts.options.point(now.position)
        
        elif key == keys.DOWN:
            opts.options.get().hover = False
            now = opts.options.next()
            now.get().hover = True
            opts.options.point(now.position)
        
        elif key == keys.PAGE_UP:
            opts.options.get().hover = False
            now = opts.options.first()
            now.get().hover = True
            opts.options.point(now.position)
        
        elif key == keys.PAGE_DOWN:
            opts.options.get().hover = False
            now = opts.options.last()
            now.get().hover = True
            opts.options.point(now.position)
        
        else:
            alert = True

def date(default: Optional[dt.date] = None) -> PromptFunction[dt.date]:
    """
    Parameters
    ----------
    default
        Default date to use. Defaults to current datetime.
    """
    if default is None:
        default = dt.date.today()
    
    selected_date = default
    
    alert = False
    while True:
        key = yield [
            Alert() if alert else None,
            Date(selected_date),
        ]
        alert = False
        
        if key == keys.LEFT:
            # prev day
            ...
        
        elif key == keys.RIGHT:
            # next day
            ...
        
        elif key in "aA":
            # prev month
            ...
        
        elif key in "dD":
            # next month
            ...
        
        else:
            alert = True


