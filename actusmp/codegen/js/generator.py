import pathlib
import typing

from actusmp.model import Contract
from actusmp.model import Dictionary
from actusmp.model import FunctionType
from actusmp.model import Term
from actusmp.codegen.js import convertors
from actusmp.utils import fsys


def gen_typeset_termsets(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    """Generates: `pyactus.typeset.terms.{contract}.js`.
    
    """
    tmpl = fsys.get_template("typeset/termset.txt")
    for contract in dictionary.contract_set:
        yield contract, tmpl.render(utils=convertors, contract=contract)


def gen_typeset_enums(dictionary: Dictionary) -> typing.Tuple[Term, str]:
    """Generates: `pyactus.typeset.enums.{enums}.js`.
    
    """
    tmpl = fsys.get_template("typeset/enum.txt")
    for definition in dictionary.enum_set:
        yield definition, tmpl.render(utils=convertors, definition=definition)


def gen_typeset_events(dictionary: Dictionary) -> str:
    """Generates: `pyactus.typeset.events.index.js`.
    
    """
    tmpl = fsys.get_template("typeset/events.txt")

    return tmpl.render(utils=convertors, dictionary=dictionary, defn=dictionary.contract_event_type)


def gen_typeset_funcs(dictionary: Dictionary) -> str:
    """Generates: `pyactus.typeset.funcs.index.js`.
    
    """
    tmpl = fsys.get_template("typeset/funcs.txt")

    return tmpl.render(utils=convertors, dictionary=dictionary)


def gen_typeset_pkg_init(dictionary: Dictionary) -> str:
    """Generates: `pyactus.typeset.index.js`.
    
    """
    tmpl = fsys.get_template("typeset/pkg_init.txt")

    return tmpl.render(utils=convertors, dictionary=dictionary)


def gen_typeset_pkg_init_enums(dictionary: Dictionary) -> str:
    """Generates: `pyactus.typeset.enums.index.js`.
    
    """
    tmpl = fsys.get_template("typeset/pkg_init_enums.txt")

    return tmpl.render(utils=convertors, dictionary=dictionary)


def gen_typeset_pkg_init_termsets(dictionary: Dictionary) -> str:
    """Generates: `pyactus.typeset.terms.index.js`.
    
    """
    tmpl = fsys.get_template("typeset/pkg_init_termsets.txt")

    return tmpl.render(utils=convertors, dictionary=dictionary)


def gen_typeset_states(dictionary: Dictionary) -> str:
    """Generates: `pyactus.typeset.states.js`.
    
    """
    tmpl = fsys.get_template("typeset/states.txt")

    return tmpl.render(utils=convertors, dictionary=dictionary)


def gen_funcset_pkg_init(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    """Generates: `pyactus.typeset.classes.{contract}.js`.
    
    """
    tmpl = fsys.get_template("funcset/pkg_init.txt")

    return tmpl.render(dictionary=dictionary, utils=convertors)


def gen_funcset_stubs_1(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    """Generates: `pyactus.funcs.{contract}.{func}_{event}_{contract}.js`.
    
    """
    tmpl_set = {
        FunctionType.POF: fsys.get_template("funcset/stub_pof.txt"),
        FunctionType.STF: fsys.get_template("funcset/stub_stf.txt")
    }

    iterator = _yield_funcset(dictionary, path_to_java_funcs)
    for contract, func_type, event_type, suffix in iterator:
        code_block = tmpl_set[func_type].render(utils=convertors, contract=contract, event_type=event_type, suffix=suffix)
        yield contract, func_type, event_type, suffix, code_block


def gen_funcset_stubs_2(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    """Generates: `pyactus.funcs.{contract}.main.js`.
    
    """
    tmpl = fsys.get_template("funcset/stub_main.txt")

    for contract in dictionary.contract_set:
        code_block = tmpl.render(utils=convertors, contract=contract)
        yield contract, code_block


def gen_funcset_stubs_pkg_init(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    """Generates: `pyactus.funcs.{contract}.index.js`.
    
    """
    tmpl = fsys.get_template("funcset/stub_pkg_init.txt")

    for contract in dictionary.contract_set:
        funcset_iterator = _yield_funcset(dictionary, path_to_java_funcs, contract)
        code_block = tmpl.render(utils=convertors, contract=contract, funcset_iterator=funcset_iterator)
        if len(code_block) > 0:
            yield contract, code_block


def _yield_funcset(
    dictionary: Dictionary,
    path_to_java_funcs: pathlib.Path,
    filter: Contract = None
) -> typing.Tuple[Contract, FunctionType, str]:
    """Yields set of functions for which code can be emitted.

    In actus-core.functions there is a sub-package for each supported contract type.
    Within each sub-package is the set of contract specific functions.  Each such
    function is named: {func-type}_{event-type}_{contract-type}.java.

    """
    for contract in dictionary.contract_set:
        if filter and filter != contract:
            continue
        path_to_java_funcs_contract = path_to_java_funcs / contract.type_info.acronym.lower()
        if path_to_java_funcs_contract.exists() and path_to_java_funcs_contract.is_dir():
            iterator = (i.stem.split("_") for i in path_to_java_funcs_contract.iterdir())
            for (func_type, event_type, suffix) in iterator:
                suffix = suffix[-1] if suffix[-1].isnumeric() else ""
                yield contract, FunctionType[func_type], event_type, suffix
