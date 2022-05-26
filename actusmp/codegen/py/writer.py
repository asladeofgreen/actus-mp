import pathlib

from actusmp.model import Dictionary
from actusmp.codegen.py.generator import gen_typeset_termsets
from actusmp.codegen.py.generator import gen_typeset_termsets_pkg_init
from actusmp.codegen.py.generator import gen_typeset_states
from actusmp.codegen.py.generator import gen_typeset_enums
from actusmp.codegen.py.generator import gen_typeset_enums_pkg_init
from actusmp.codegen.py.generator import gen_typeset_pkg_init
from actusmp.codegen.py.generator import gen_funcset_pkg_init
from actusmp.codegen.py.generator import gen_funcset_stubs_1
from actusmp.codegen.py.generator import gen_funcset_stubs_2
from actusmp.codegen.py.generator import gen_funcset_stubs_pkg_init
from actusmp.utils.convertors import to_underscore_case


def write_typeset(dest: pathlib.Path, dictionary: Dictionary):
    """Writes code files to `pyactus`.

    :param dest: Path to directory to which code will be emitted.
    :param dictionary: Deserialised actus-dictionary.json.

    """
    for writer in (
        _write_typeset_dirs,
        _write_typeset_pkg_init,
        _write_typeset_termsets,
        _write_typeset_termsets_pkg_init,
        _write_typeset_states,
        _write_typeset_enums,
        _write_typeset_enums_pkg_init,
    ):
        writer(dictionary, dest)


def write_funcset(
    dest: pathlib.Path,
    dictionary: Dictionary,
    path_to_java_impl: pathlib.Path
):
    """Writes to file system set of actus function stubs (to be subsequently completed by developer).

    :param dest: Path to directory to which code will be emitted.
    :param dictionary: Deserialised actus-dictionary.json.
    :param path_to_java_impl: Path to actus-code Java library from which funcs will be derived.
    
    """
    path_to_java_funcs = path_to_java_impl / "src" / "main" / "java" / "org" / "actus" / "functions"
    assert path_to_java_funcs.exists() and path_to_java_funcs.is_dir()

    _write_funcset_pkg_init(dictionary, dest, path_to_java_funcs)
    _write_funcset_stubs_1(dictionary, dest, path_to_java_funcs)
    _write_funcset_stubs_2(dictionary, dest)
    _write_funcset_stubs_pkg_init(dictionary, dest, path_to_java_funcs)


def _write_funcset_pkg_init(
    dictionary: Dictionary,
    dest: pathlib.Path,
    path_to_java_funcs: pathlib.Path
):
    code_block = gen_funcset_pkg_init(dictionary, path_to_java_funcs)
    dpath = dest / "funcset"
    dpath.mkdir(parents=True, exist_ok=True)
    with open(dpath / "__init__.py", "w") as fstream:
        fstream.write(code_block)


def _write_funcset_stubs_1(
    dictionary: Dictionary,
    dest: pathlib.Path,
    path_to_java_funcs: pathlib.Path
):
    """Writes to `pyactus.funcs.{contract}.{func_type}_{event_type}_{contract}.py`.
    
    """    
    for contract, func_type, event_type, suffix, code_block in gen_funcset_stubs_1(dictionary, path_to_java_funcs):
        contract_type = contract.acronym.lower()
        func_type = func_type.name.lower()
        event_type = event_type.lower()

        dpath = dest / "funcset" / contract_type
        dpath.mkdir(parents=True, exist_ok=True)

        if suffix != "":
            fpath = dpath / f"{func_type}_{event_type}_{suffix}.py"
        else:
            fpath = dpath / f"{func_type}_{event_type}.py"

        with open(fpath, "w") as fstream:
            fstream.write(code_block)


def _write_funcset_stubs_2(
    dictionary: Dictionary,
    dest: pathlib.Path
):
    """Writes to `pyactus.funcs.{contract}.main.py`.
    
    """    
    for contract, code_block in gen_funcset_stubs_2(dictionary):
        dpath = dest / "funcset" / contract.acronym.lower()
        dpath.mkdir(parents=True, exist_ok=True)
        fpath = dpath / "main.py"
        with open(fpath, "w") as fstream:
            fstream.write(code_block)


def _write_funcset_stubs_pkg_init(
    dictionary: Dictionary,
    dest: pathlib.Path,
    path_to_java_funcs: pathlib.Path
):
    """Writes to `pyactus.funcs.{contract}.{func_type}_{event_type}_{contract}.py`.
    
    """    
    for contract, code_block in gen_funcset_stubs_pkg_init(dictionary, path_to_java_funcs):
        dpath = dest / "funcset" / contract.acronym.lower()
        dpath.mkdir(parents=True, exist_ok=True)
        with open(dpath / "__init__.py", "w") as fstream:
            fstream.write(code_block)


def _write_typeset_dirs(dictionary: Dictionary, dest: pathlib.Path):
    """Writes directories to `pyactus.typeset`.
    
    """
    for dpath in (
        dest / "typeset" / "enums",
        dest / "typeset" / "termsets"
    ):
        dpath.mkdir(parents=True, exist_ok=True)


def _write_typeset_enums(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.enums.{enum}.py`.
    
    """
    for term, code_block in gen_typeset_enums(dictionary):
        fpath = dest / "typeset" / "enums" / f"{to_underscore_case(term.identifier)}.py"
        with open(fpath, "w") as fstream:
            fstream.write(code_block)


def _write_typeset_enums_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.enums.__init__.py`.
    
    """
    code_block = gen_typeset_enums_pkg_init(dictionary)
    with open(dest / "typeset" / "enums" / "__init__.py", "w") as fstream:
        fstream.write(code_block)


def _write_typeset_states(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.states.py`.
    
    """
    code_block = gen_typeset_states(dictionary)
    with open(dest / "typeset" / "states.py", "w") as fstream:
        fstream.write(code_block)


def _write_typeset_termsets(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.termsets.{contract}.py`.
    
    """
    for contract, code_block in gen_typeset_termsets(dictionary):
        fpath = dest / "typeset" / "termsets" / f"{to_underscore_case(contract.identifier)}.py"
        with open(fpath, "w") as fstream:
            fstream.write(code_block)


def _write_typeset_termsets_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.termsets.__init__.py`.
    
    """
    code_block = gen_typeset_termsets_pkg_init(dictionary)
    with open(dest / "typeset" / "termsets" / "__init__.py", "w") as fstream:
        fstream.write(code_block)


def _write_typeset_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.__init__.py`.
    
    """
    code_block = gen_typeset_pkg_init(dictionary)
    with open(dest / "typeset" / "__init__.py", "w") as fstream:
        fstream.write(code_block)
