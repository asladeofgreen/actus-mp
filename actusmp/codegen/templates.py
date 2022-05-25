import os
import pathlib
import typing

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


# Set resource home folder.
_DIR: pathlib.Path = pathlib.Path(os.path.dirname(__file__))

# Set template sub-folders.
_SUB_DIRS: typing.List[pathlib.Path] = [
    _DIR / "js" / "templates",
    _DIR / "py" / "templates",
    _DIR / "rs" / "templates",
]

# Set template engine.
_TEMPLATE_ENV: Environment = Environment(
    loader=FileSystemLoader(_SUB_DIRS),
    autoescape=select_autoescape(),
    trim_blocks=True
)

# Set template loading function.
get_template: typing.Callable = _TEMPLATE_ENV.get_template
