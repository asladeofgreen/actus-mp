import pathlib

from actusmp.model import Dictionary
from actusmp.codegen.ts import generator
from actusmp.utils import fsys
from actusmp.utils.convertors import to_pascal_case


def write_typeset(dest: pathlib.Path, dictionary: Dictionary):
    """Writes code files to `actusjs`.

    :param dest: Path to directory to which code will be emitted.
    :param dictionary: Deserialised actus-dictionary.json.

    """
    def _yield_code():
        # Termsets.
        for defn, code_block in generator.gen_contracts_terms(dictionary):
            yield code_block, \
                  dest / "terms" / f"{defn.type_info.acronym.lower()}.ts"
        
        # Termset index.
        yield generator.gen_contracts_terms_index(dictionary), \
              dest / "terms" / "index.ts"

        # Enums.
        for defn, code_block in generator.gen_enums(dictionary):
            yield code_block, \
                  dest / "enums" / f"{to_pascal_case(defn.identifier)}.ts"

        # Enum index.
        yield generator.gen_enums_index(dictionary), \
              dest / "enums" / "index.ts", \

        # State space.
        yield generator.gen_state_space(dictionary), \
              dest / "core" / "states.ts"

    fsys.write_code(_yield_code)


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
    # The JAVA implementation (see actus-core) exposes a set of functions. By scanning them 
    # we can partially determine which stubs should be be generated.
    path_to_java_funcs = path_to_java_impl / "src" / "main" / "java" / "org" / "actus" / "functions"
    assert path_to_java_funcs.exists() and path_to_java_funcs.is_dir()

    def _yield_code():
        # Index.
        yield generator.gen_funcset_index(dictionary, path_to_java_funcs), \
              dest / "funcs" / "index.ts"
            
        # Function stubs.
        for defn, func_type, event_type, suffix, code_block in generator.gen_func_stubs(dictionary, path_to_java_funcs):
            fname = f"{func_type.name.lower()}_{event_type}"
            fname = f"{fname}_{suffix}.ts" if suffix else f"{fname}.ts"
            yield code_block, \
                    dest / "funcs" / f"{defn.type_info.acronym.lower()}" / fname
                    
        # Function stubs: index.
        for defn, code_block in generator.gen_func_stubs_index(dictionary, path_to_java_funcs):
            yield code_block, \
                  dest / "funcs" / f"{defn.type_info.acronym.lower()}" / "index.ts" 
                  
        # Function stubs: main.
        for defn, code_block in generator.gen_func_stubs_main(dictionary):
            yield code_block, \
                  dest / "funcs" / f"{defn.type_info.acronym.lower()}" / "main.ts" 

    fsys.write_code(_yield_code)
