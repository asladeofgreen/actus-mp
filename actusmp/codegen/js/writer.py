import code
import pathlib

from actusmp.model import Dictionary

from actusmp.codegen.js.generator import gen_typeset_core_enum
from actusmp.codegen.js.generator import gen_typeset_core_enum_index

from actusmp.codegen.js.generator import gen_typeset_core_index
from actusmp.codegen.js.generator import gen_typeset_core_states
from actusmp.codegen.js.generator import gen_typeset_termsets
from actusmp.codegen.js.generator import gen_typeset_pkg_init_termsets
from actusmp.codegen.js.generator import gen_typeset_enums
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
    def _yield_dirs():
        yield dest / "typeset" / "enums"
        yield dest / "typeset" / "core" / "enums"
        yield dest / "typeset" / "terms"

    def _yield_core_enums():
        for defn in dictionary.enum_set_core:
            yield \
                dest / "typeset" / "core" / "enums" / f"{defn.identifier}.ts", \
                gen_typeset_core_enum(dictionary, defn)
        yield \
            dest / "typeset" / "core" / "enums" / "index.ts", \
            gen_typeset_core_enum_index(dictionary)

    def _yield_core_index():
        yield \
            dest / "typeset" / "core" / "index.ts", \
            gen_typeset_core_index(dictionary)

    def _yield_core_states():
        yield \
            dest / "typeset" / "core" / "states.ts", \
            gen_typeset_core_states(dictionary)

    def _yield_term_defns():
        for contract, code_block in gen_typeset_termsets(dictionary):
            yield \
                dest / "typeset" / "terms" / f"{to_pascal_case(contract.type_info.identifier)}.ts", \
                code_block
        yield \
            dest / "typeset" / "terms" / "index.ts", \
            gen_typeset_pkg_init_termsets(dictionary)

    def _yield_term_enums():
        for term, code_block in gen_typeset_enums(dictionary):
            yield \
                dest / "typeset" / "enums" / f"{to_pascal_case(term.identifier)}.ts", \
                code_block
        yield \
            dest / "typeset" / "enums" / "index.ts", \
            gen_typeset_pkg_init_enums(dictionary)

    def _yield_index():
        yield \
            dest / "typeset" / "index.ts", \
            gen_typeset_pkg_init(dictionary)

    # Prepare file system.
    for path_to_dir in _yield_dirs():
        path_to_dir.mkdir(parents=True, exist_ok=True)

    # Write code files.
    for factory in (
        _yield_core_enums,
        _yield_core_index,
        _yield_core_states,
        _yield_index,
        _yield_term_defns,
        _yield_term_enums,
    ):
        for fpath, code_block in factory():
            fsys.write(fpath, code_block)


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

    def _yield_dirs():
        yield dest / "funcset"
        for contract in dictionary.contract_set:
            yield dest / "funcset" / contract.type_info.acronym.lower()

    def _yield_index():
        yield \
            dest / "funcset" / "index.ts", \
            gen_funcset_pkg_init(dictionary, path_to_java_funcs)

    def _yield_stubs_1():
        for _, func_type, event_type, suffix, code_block in gen_funcset_stubs_1(dictionary, path_to_java_funcs):
            if suffix != "":
                yield \
                    dest / "funcset" / f"{func_type.name.lower()}_{event_type.lower()}_{suffix}.ts", \
                    code_block
            else:
                yield \
                    dest / "funcset" / f"{func_type.name.lower()}_{event_type.lower()}.ts", \
                    code_block

    def _yield_stubs_2():
        for _, code_block in gen_funcset_stubs_2(dictionary):
            yield \
                dest / "funcset" / "main.js", \
                code_block

    def _yield_stubs_index():
        for _, code_block in gen_funcset_stubs_pkg_init(dictionary, path_to_java_funcs):
            yield \
                dest / "funcset" / "index.js", \
                code_block

    # Prepare file system.
    for path_to_dir in _yield_dirs():
        path_to_dir.mkdir(parents=True, exist_ok=True)

    # Write code files.
    for factory in (
        _yield_index,
        _yield_stubs_1,
        _yield_stubs_2,
        _yield_stubs_index,
    ):
        for fpath, code_block in factory():
            fsys.write(fpath, code_block)
    