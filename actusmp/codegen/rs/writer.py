import pathlib

from actusmp.model import Dictionary


def write_typeset(dest: pathlib.Path, dictionary: Dictionary):
    """Writes code files to `actus-rs`.

    :param dest: Path to directory to which code will be emitted.
    :param dictionary: Deserialised actus-dictionary.json.

    """
    raise NotImplementedError()


def write_funcset(
    dest: pathlib.Path,
    dictionary: Dictionary,
    path_to_java_impl: pathlib.Path,
    force: bool
):
    """Writes to file system set of actus function stubs (to be subsequently completed by developer).

    :param dest: Path to directory to which code will be emitted.
    :param dictionary: Deserialised actus-dictionary.json.
    :param path_to_java_impl: Path to actus-code Java library from which funcs will be derived.
    :param force: Flag instructing generator to overwrite existing files or not. 
    
    """
    raise NotImplementedError()
