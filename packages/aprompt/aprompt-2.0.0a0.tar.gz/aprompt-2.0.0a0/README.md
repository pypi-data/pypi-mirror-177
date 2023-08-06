aprompt - **A**dvanced **P**rompts
==================================

aprompt provides a large set of prompts and
corresponding themes as well as support for
testing prompts. aprompt is designed for
creating own prompts and themes.


Available Prompts
-----------------

* [x] Text
* [x] Secret
* [ ] Digit Code
* [x] Integer
* [ ] Sort
* [x] Choice
* [x] Multiple Choice
* [ ] Confirmation
* [ ] Datetime
* [ ] Date
* [ ] Time


Features
--------

* [x] Creation of custom prompts.
* [x] Creation of custom themes.
* [x] Testing features.
* [x] Examples and tutorials demonstrating the prompts.


Installation
------------

```bash
pip install aprompt
```


Basic Usage
-----------

```python
from aprompt import prompt, prompts

username = prompt(
    "Please enter your username.",
    prompts.text()
)

email = prompt(
    "Please enter an email.",
    prompts.text()
)

password = prompt(
    "Please set a password.",
    prompts.text(hide = True),
    validate = lambda x: Exception("password too short") if len(x) < 7 else None,
)
```


Links
-----

* [Documentation](https://phoenixr-codes.github.io/aprompt/)
* [Source Code](https://github.com/phoenixr-codes/aprompt/)
* [PyPI](https://pypi.org/prpject/aprompt)
