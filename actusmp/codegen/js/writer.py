import pathlib

from actusmp.model import Dictionary
from actusmp.codegen.js.generator import gen_typeset_termsets
from actusmp.codegen.js.generator import gen_typeset_pkg_init_termsets
from actusmp.codegen.js.generator import gen_typeset_states
from actusmp.codegen.js.generator import gen_typeset_enums
from actusmp.codegen.js.generator import gen_typeset_events
from actusmp.codegen.js.generator import gen_typeset_funcs
from actusmp.codegen.js.generator import gen_typeset_pkg_init_enums
from actusmp.codegen.js.generator import gen_typeset_pkg_init
from actusmp.codegen.js.generator import gen_funcset_pkg_init
from actusmp.codegen.js.generator import gen_funcset_stubs_1
from actusmp.codegen.js.generator import gen_funcset_stubs_2
from actusmp.codegen.js.generator import gen_funcset_stubs_pkg_init
from actusmp.utils import fsys
from actusmp.utils.convertors import to_pascal_case


def write_typeset(dest: pathlib.Path, dictionary: Dictionary):
    """Writes code files to `actusjs`.

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
        _write_typeset_events,
        _write_typeset_funcs,
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
    """Writes to `actusjs.funcset.{contract}.{func_type}_{event_type}_{contract}`.
    
    """
    dpath = dest / "funcset"
    dpath.mkdir(parents=True, exist_ok=True)
    fpath = dpath / "index.ts"
    code_block = gen_funcset_pkg_init(dictionary, path_to_java_funcs)
    fsys.write(fpath, code_block)


def _write_funcset_stubs_1(
    dictionary: Dictionary,
    dest: pathlib.Path,
    path_to_java_funcs: pathlib.Path
):
    """Writes to `actusjs.funcset.{contract}.{func_type}_{event_type}_{contract}`.
    
    """    
    for contract, func_type, event_type, suffix, code_block in gen_funcset_stubs_1(dictionary, path_to_java_funcs):
        dpath = dest / "funcset" / contract.type_info.acronym.lower()
        dpath.mkdir(parents=True, exist_ok=True)
        if suffix != "":
            fpath = dpath / f"{func_type.name.lower()}_{event_type.lower()}_{suffix}.ts"
        else:
            fpath = dpath / f"{func_type.name.lower()}_{event_type.lower()}.ts"
        fsys.write(fpath, code_block)


def _write_funcset_stubs_2(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.funcset.{contract}.main`.
    
    """    
    for contract, code_block in gen_funcset_stubs_2(dictionary):
        dpath = dest / "funcset" / contract.type_info.acronym.lower()
        dpath.mkdir(parents=True, exist_ok=True)
        fpath = dpath / "main.js"
        fsys.write(fpath, code_block)


def _write_funcset_stubs_pkg_init(
    dictionary: Dictionary,
    dest: pathlib.Path,
    path_to_java_funcs: pathlib.Path
):
    """Writes to `actusjs.funcset.{contract}.{func_type}_{event_type}_{contract}`.
    
    """    
    for contract, code_block in gen_funcset_stubs_pkg_init(dictionary, path_to_java_funcs):
        dpath = dest / "funcset" / contract.type_info.acronym.lower()
        dpath.mkdir(parents=True, exist_ok=True)
        fpath = dpath / "index.js"
        fsys.write(fpath, code_block)


def _write_typeset_dirs(_: Dictionary, dest: pathlib.Path):
    """Writes directories to `actusjs.typeset`.
    
    """
    for dpath in (
        dest / "typeset" / "enums",
        dest / "typeset" / "events",
        dest / "typeset" / "funcs",
        dest / "typeset" / "states",
        dest / "typeset" / "terms"
    ):
        dpath.mkdir(parents=True, exist_ok=True)


def _write_typeset_enums(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.typeset.enums.{enum}`.
    
    """
    for term, code_block in gen_typeset_enums(dictionary):
        fpath = dest / "typeset" / "enums" / f"{to_pascal_case(term.identifier)}.ts"
        fsys.write(fpath, code_block)


def _write_typeset_enums_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.typeset.enums.index`.
    
    """
    fpath = dest / "typeset" / "enums" / "index.ts"
    code_block = gen_typeset_pkg_init_enums(dictionary)
    fsys.write(fpath, code_block)


def _write_typeset_events(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.typeset.events.index`.
    
    """
    fpath = dest / "typeset" / "events" / "index.ts"
    code_block = gen_typeset_events(dictionary)
    fsys.write(fpath, code_block)


def _write_typeset_funcs(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.typeset.events.index`.
    
    """
    fpath = dest / "typeset" / "funcs" / "index.ts"
    code_block = gen_typeset_funcs(dictionary)
    fsys.write(fpath, code_block)


def _write_typeset_states(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.typeset.states`.
    
    """
    fpath = dest / "typeset" / "states" / "index.ts"
    code_block = gen_typeset_states(dictionary)
    fsys.write(fpath, code_block)


def _write_typeset_termsets(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.typeset.termsets.{contract}`.
    
    """
    for contract, code_block in gen_typeset_termsets(dictionary):
        fpath = dest / "typeset" / "terms" / f"{to_pascal_case(contract.type_info.identifier)}.ts"
        fsys.write(fpath, code_block)


def _write_typeset_termsets_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.typeset.termsets.index`.
    
    """
    fpath = dest / "typeset" / "terms" / "index.ts"
    code_block = gen_typeset_pkg_init_termsets(dictionary)
    fsys.write(fpath, code_block)


def _write_typeset_pkg_init(dictionary: Dictionary, dest: pathlib.Path):
    """Writes to `actusjs.typeset.index`.
    
    """
    fpath = dest / "typeset" / "index.ts"
    code_block = gen_typeset_pkg_init(dictionary)
    fsys.write(fpath, code_block)
