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
from actusmp.utils import fsystem
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
    # The JAVA implementation, actus-core, exposes a set of functions, we scan 
    # these to determine which stubs should be be generated.
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
    """Writes to `pyactus.funcset.{contract}.{func_type}_{event_type}_{contract}.py`.
    
    """
    dpath = dest / "funcset"
    dpath.mkdir(parents=True, exist_ok=True)
    fpath = dpath / "__init__.py"
    code_block = gen_funcset_pkg_init(dictionary, path_to_java_funcs)
    fsystem.write(fpath, code_block)


def _write_funcset_stubs_1(
    dictionary: Dictionary,
    dest: pathlib.Path,
    path_to_java_funcs: pathlib.Path
):
    """Writes to `pyactus.funcset.{contract}.{func_type}_{event_type}_{contract}.py`.
    
    """    
    for contract, func_type, event_type, suffix, code_block in gen_funcset_stubs_1(dictionary, path_to_java_funcs):
        dpath = dest / "funcset" / contract.type_info.acronym.lower()
        dpath.mkdir(parents=True, exist_ok=True)
        if suffix != "":
            fpath = dpath / f"{func_type.name.lower()}_{event_type.lower()}_{suffix}.py"
        else:
            fpath = dpath / f"{func_type.name.lower()}_{event_type.lower()}.py"
        fsystem.write(fpath, code_block)


def _write_funcset_stubs_2(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.funcset.{contract}.main.py`.
    
    """    
    for contract, code_block in gen_funcset_stubs_2(dictionary):
        dpath = dest / "funcset" / contract.type_info.acronym.lower()
        dpath.mkdir(parents=True, exist_ok=True)
        fpath = dpath / "main.py"
        fsystem.write(fpath, code_block)


def _write_funcset_stubs_pkg_init(
    dictionary: Dictionary,
    dest: pathlib.Path,
    path_to_java_funcs: pathlib.Path
):
    """Writes to `pyactus.funcset.{contract}.{func_type}_{event_type}_{contract}.py`.
    
    """    
    for contract, code_block in gen_funcset_stubs_pkg_init(dictionary, path_to_java_funcs):
        dpath = dest / "funcset" / contract.type_info.acronym.lower()
        dpath.mkdir(parents=True, exist_ok=True)
        fpath = dpath / "__init__.py"
        fsystem.write(fpath, code_block)


def _write_typeset_dirs(_: Dictionary, dest: pathlib.Path):
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
        fsystem.write(fpath, code_block)


def _write_typeset_enums_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.enums.__init__.py`.
    
    """
    fpath = dest / "typeset" / "enums" / "__init__.py"
    code_block = gen_typeset_enums_pkg_init(dictionary)
    fsystem.write(fpath, code_block)


def _write_typeset_states(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.states.py`.
    
    """
    fpath = dest / "typeset" / "states.py"
    code_block = gen_typeset_states(dictionary)
    fsystem.write(fpath, code_block)


def _write_typeset_termsets(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.termsets.{contract}.py`.
    
    """
    for contract, code_block in gen_typeset_termsets(dictionary):
        fpath = dest / "typeset" / "termsets" / f"{to_underscore_case(contract.type_info.identifier)}.py"
        fsystem.write(fpath, code_block)


def _write_typeset_termsets_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.termsets.__init__.py`.
    
    """
    fpath = dest / "typeset" / "termsets" / "__init__.py"
    code_block = gen_typeset_termsets_pkg_init(dictionary)
    fsystem.write(fpath, code_block)


def _write_typeset_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `pyactus.typeset.__init__.py`.
    
    """
    fpath = dest / "typeset" / "__init__.py"
    code_block = gen_typeset_pkg_init(dictionary)
    fsystem.write(fpath, code_block)
