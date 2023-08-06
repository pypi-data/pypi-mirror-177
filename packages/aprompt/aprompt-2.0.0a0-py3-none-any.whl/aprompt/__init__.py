from __future__ import annotations

from collections.abc import Callable, Generator, Iterator, Iterable
from functools import partial
from pprint import PrettyPrinter
import signal
import sys
from typing import Optional, overload, TypeVar, Literal

import readchar
from readchar import key as keys

from . import containers
from . import themes
from .prompts import PromptFunction
from ._utils import clear_lines, display, termsize

T = TypeVar("T")


pretty_printer = partial(PrettyPrinter)
"""
Partially initialized pretty printer used for debugging.
This may be overriden by another ``functools.partial<PrettyPrinter>``
instance for custom appearance.

``width`` and ``stream`` are passed before
calling ``.pprint()``.
"""

def prompt(
    ask: str,
    prompt_fn: PromptFunction[T],
    *,
    validate: Optional[Union[
        Callable[[T], Optional[BaseException]],
        Callable[[T], bool]
    ]] = None,
    file: Optional[TextIO] = None,
    theme: Optional[Theme] = None,
    teardown: Callable[[], None] = None,
    debug: bool = False,
    test_with: Optional[Iterator[str]] = None,
) -> T:
    r"""
    Prompts a message to the user.
    
    This function is a wrapper around the actual prompt
    function (``prompt_fn``). It
    reads keys, sends them to the prompt function and
    prints the result formatted by the ``theme``. This
    function also handles validation, termination and
    more.
    
    Parameters
    ----------
    ask
        The question/message to prompt.
    
    prompt_fn
        A prompt function.
    
    validate
        A callable taking the result as the
        argument and returning a ``BaseException``
        to repeat the function or ``None`` to
        pass.
        
        Alternatively, a callable that returns
        a boolean may be used. This variant however
        will not display any error message and
        insteads trigger the bell (``'\a'``).
        
        If not given, no check will be done.
    
    file
        The file or file-like object to write to.
        Defaults to the standard output.
    
    theme
        The theme to use for this prompt.
        Defaults to a new instance of
        :class:`themes.Basic`.
    
    teardown
        A callable that takes no arguments and
        returns nothing that is called when the
        user hits ``CTRL + C``. The programm will
        be terminated afterwards. This is a shorthand
        for::
            
            try:
                prompt(...)
            except SystemExit as exc:
                teardown()
                raise exc
    
    debug
        Prints the :class:`containers.Container`\s
        instead of formatting them.
    
    test_with
        Optional iterable of strings to send to the
        prompt. Useful for writing tests.
    
    Raises
    ------
    ``SystemExit``
        User hit ``CTRL + C``.
    
    """
    if file is None:
        file = sys.stdout
    
    if theme is None:
        theme = themes.Basic()
    
    theme._init(termsize(file))
    
    conts = [
        containers.Question(message = ask),
        *prompt_fn.send(None)
    ]
    
    clear = 0
    
    while True:
        if debug and test_with is None:
            pp = pretty_printer(
                width = termsize(file).columns,
                stream = file,
            )
            pp.pprint(conts)
        
        elif test_with is None:
            disp = display(
                *conts,
                theme = theme,
                file = file,
            )
            
            print(
                clear_lines(clear),
                disp,
                file = file,
                flush = True,
                sep = "",
                end = "",
            )
            clear = disp.count("\n")
        
        conts = [containers.Question(message = ask)]
        
        if test_with is None:
            key = readchar.readkey()
        else:
            try:
                key = next(test_with)
            except StopIteration:
                raise RuntimeError("prompt has never finished")
        
        if key == keys.CTRL_C:
            if teardown is not None: teardown()
            if not debug and test_with is None: print(file = file, flush = True)
            sys.exit(signal.SIGINT)
        
        try:
            c = prompt_fn.send(key)
        except Exception as exc:
            conts.append(containers.Error(exc))
        
        if isinstance(c, containers.Final):
            if not debug and test_with is None: print(file = file, flush = True)
            if validate is not None:
                res = validate(c.content)
                
                if isinstance(res, BaseException):
                    conts.insert(0, containers.Error(res))
                
                elif res is None or not res:
                    conts.insert(0, containers.Error(Exception()))
                
                else:
                    return c.content
            
            else:
                return c.content
        
        else:
            conts.extend(c)
        
        
