import os
import pathlib
import typing

import jinja2

from actusmp import model


# Set templates home folder.
_TEMPLATES_DIR: pathlib.Path = pathlib.Path(os.path.dirname(__file__)).parent / "templates"

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
    if not fpath.parent.exists():
        fpath.parent.mkdir(parents=True)
    with open(fpath, "w") as fstream:
        fstream.write(content)


def yield_funcset(
    dictionary: model.Dictionary,
    path_to_java_funcs: pathlib.Path,
    f_type: model.FunctionType
) -> typing.Tuple[model.Contract, model.FunctionType, str]:
    """Yields set of functions for which code can be emitted.

    In actus-core.functions there is a sub-package for each supported contract type.
    Within each sub-package is the set of contract specific functions.  Each such
    function is named: {func-type}_{event-type}_{contract-type}.java.

    :param dictionary: ACTUS dictionary wrapper.
    :param path_to_java_funcs: Path to functions defined in actus-core.
    :param f_type: Type of ACTUS function to be processed.
    :returns: Iterator over set of functions declared in actus-core.

    """
    for contract in dictionary.contract_set:
        path_to_java_funcs_contract = path_to_java_funcs / contract.type_info.acronym.lower()
        if path_to_java_funcs_contract.exists() and path_to_java_funcs_contract.is_dir():
            iterator = (i.stem.split("_") for i in path_to_java_funcs_contract.iterdir())
            for (func_type, event_type, suffix) in iterator:
                if f_type.name == func_type:
                    suffix = suffix[-1] if suffix[-1].isnumeric() else ""
                    yield contract, event_type, suffix
