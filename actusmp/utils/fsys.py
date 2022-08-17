import os
import pathlib
import typing

import jinja2


# Set templates home folder.
_TEMPLATES_DIR: pathlib.Path = pathlib.Path(os.path.dirname(__file__)).parent / "templates"

# Set codegen template sub-folders.
_TEMPLATES_DIR: typing.List[pathlib.Path] = [
    _TEMPLATES_DIR / "js",
    _TEMPLATES_DIR / "py",
    _TEMPLATES_DIR / "rs"
]

# Set codegen template engine.
_CODEGEN_ENV: jinja2.Environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(_TEMPLATES_DIR),
    autoescape=jinja2.select_autoescape(),
    trim_blocks=True
)

# Set template loading function.
get_template: typing.Callable = _CODEGEN_ENV.get_template


def write(fpath: pathlib.Path, content: str):
    """Simple sink function to write file contents to file system.

    Useful so as to simplify suspending writing when testing.

    :param fpath: Target file path.
    :param content: File content to be written.
    
    """
    with open(fpath, "w") as fstream:
        fstream.write(content)
