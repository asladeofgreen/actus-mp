import pathlib
import typing

from actusmp.model import Contract
from actusmp.model import Dictionary
from actusmp.model import FunctionType
from actusmp.model import Term
from actusmp.codegen.ts import convertor
from actusmp.utils import fsys


def gen_contracts_terms_index(dictionary: Dictionary) -> str:
    tmpl = fsys.get_template("termset_index.txt")

    return tmpl.render(dictionary=dictionary, utils=convertor)

def gen_enums(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    tmpl = fsys.get_template("enum.txt")
    for defn in dictionary.enum_set:
        yield defn, tmpl.render(defn=defn, utils=convertor)

def gen_enums_index(dictionary: Dictionary) -> str:
    tmpl = fsys.get_template("enum_index.txt")

    return tmpl.render(utils=convertor, dictionary=dictionary)

def gen_state_space(dictionary: Dictionary) -> str:
    tmpl = fsys.get_template("state_space.txt")

    return tmpl.render(utils=convertor, dictionary=dictionary)

def gen_contracts_terms(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    tmpl = fsys.get_template("termset.txt")
    for defn in dictionary.contract_set:
        yield defn, tmpl.render(defn=defn, utils=convertor)


def gen_funcset_index(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    tmpl = fsys.get_template("func_index.txt")

    return tmpl.render(dictionary=dictionary, utils=convertor)

def gen_func_stubs(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    tmpl_set = {
        FunctionType.POF: fsys.get_template("func_stub_pof.txt"),
        FunctionType.STF: fsys.get_template("func_stub_stf.txt")
    }
    iterator = fsys.yield_funcset(dictionary, path_to_java_funcs)
    for contract, func_type, event_type, suffix in iterator:
        yield contract, func_type, event_type, suffix, tmpl_set[func_type].render(
            contract=contract,
            event_type=event_type,
            suffix=suffix,
            utils=convertor,
            )

def gen_func_stubs_index(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    tmpl = fsys.get_template("func_stub_index.txt")
    for defn in dictionary.contract_set:
        iterator = fsys.yield_funcset(dictionary, path_to_java_funcs, defn)
        yield defn, tmpl.render(utils=convertor, contract=defn, funcset_iterator=iterator)
        
def gen_func_stubs_main(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    tmpl = fsys.get_template("func_stub_main.txt")
    for defn in dictionary.contract_set:
        yield defn, tmpl.render(defn=defn, utils=convertor)
