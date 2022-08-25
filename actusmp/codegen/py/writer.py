import pathlib

from actusmp.model import Dictionary
from actusmp.codegen.py import generator
from actusmp.utils import fsys
from actusmp.utils.convertors import to_underscore_case


def write_typeset(dest: pathlib.Path, dictionary: Dictionary):
    """Writes code files to `pyactus`.

    :param dest: Path to directory to which code will be emitted.
    :param dictionary: Deserialised actus-dictionary.json.

    """
    def _yield_code():
        # Terms.
        for defn, code_block in generator.gen_terms(dictionary):
            yield code_block, dest / "terms" / f"{defn.type_info.acronym.lower()}.py"
        
        # Terms index.
        yield generator.gen_terms_index(dictionary), \
              dest / "terms" / "__init__.py"

        # Enums.
        for defn, code_block in generator.gen_enums(dictionary):
            yield code_block, \
                  dest / "enums" / f"{to_underscore_case(defn.identifier)}.py"

        # Enums index.
        yield generator.gen_enums_index(dictionary), \
              dest / "enums" / "__init__.py", \

        # States.
        yield generator.gen_state_space(dictionary), \
              dest / "core" / "states.py"

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
    # The JAVA implementation, actus-core, exposes a set of functions, we scan 
    # these to determine which stubs should be be generated.
    path_to_java_funcs = path_to_java_impl / "src" / "main" / "java" / "org" / "actus" / "functions"
    assert path_to_java_funcs.exists() and path_to_java_funcs.is_dir()

    def _yield_code():
        # Index.
        yield generator.gen_func_index(dictionary, path_to_java_funcs), \
              dest / "funcs" / "__init__.py"

        # Function stubs.
        for defn, func_type, event_type, suffix, code_block in generator.gen_func_stubs(dictionary, path_to_java_funcs):
            fname = f"{func_type.name.lower()}_{event_type}"
            fname = f"{fname}_{suffix}.ts" if suffix else f"{fname}.py"
            yield code_block, \
                    dest / "funcs" / f"{defn.type_info.acronym.lower()}" / fname

        # Function stubs: index.
        for defn, code_block in generator.gen_func_stubs_index(dictionary, path_to_java_funcs):
            yield code_block, \
                  dest / "funcs" / f"{defn.type_info.acronym.lower()}" / "__init__.py" 

        # Function stubs: main.
        for defn, code_block in generator.gen_func_stubs_main(dictionary):
            yield code_block, \
                  dest / "funcs" / f"{defn.type_info.acronym.lower()}" / "main.py" 

    fsys.write_code(_yield_code)
