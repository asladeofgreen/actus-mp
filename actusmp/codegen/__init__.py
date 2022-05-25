import enum
import pathlib

from actusmp.codegen.py import writer as python_writer
from actusmp.codegen.rs import writer as rust_writer
from actusmp.dictionary import get_dictionary


class TargetLanguage(enum.Enum):
    """Enumeration over set of supported language targets.
    
    """
    python = enum.auto()
    rust = enum.auto()


# Map: target language type <-> code generator.
_WRITERS = {
    TargetLanguage.python: python_writer,
    TargetLanguage.rust: rust_writer,
}


def write_typeset(lang: TargetLanguage, dest: pathlib.Path):
    """Writes to file system actus typeset in target langauge.
    
    :param lang: Target progamming language.
    :param dest: Path to directory to which code will be emitted.

    """
    assert lang in _WRITERS
    assert dest.exists() and dest.is_dir()

    _WRITERS[lang].write_typeset(dest, get_dictionary())


def write_funcset(
    lang: TargetLanguage, 
    dest: pathlib.Path,
    path_to_java_impl: pathlib.Path
):
    """Writes to file system set of actus function stubs (to be subsequently completed by developer).

    :param lang: Target progamming language.
    :param dest: Path to directory to which code will be emitted.
    :param path_to_java_impl: Path to actus-code Java library from which funcs will be derived.
    
    """
    assert lang in _WRITERS
    assert dest.exists and dest.is_dir
    assert path_to_java_impl.exists() and path_to_java_impl.is_dir()

    _WRITERS[lang].write_funcset(dest, get_dictionary(), path_to_java_impl)
