from enum import unique
import pathlib
import typing

from actusmp.model import Contract
from actusmp.model import Dictionary
from actusmp.model import FunctionType
from actusmp.model import Term
from actusmp.codegen.py import convertors
from actusmp.utils import fsys
from actusmp.utils.generators import gen_many
from actusmp.utils.generators import gen_one


def gen_enums(dictionary: Dictionary) -> typing.Tuple[Term, str]:
    for defn, code_block in gen_many("enum.txt", dictionary.enum_set, convertors):
        yield defn, code_block

def gen_enums_index(dictionary: Dictionary) -> str:
    return gen_one("enum_index.txt", dictionary, convertors)

def gen_state_space(dictionary: Dictionary) -> str:
    return gen_one("state_space.txt", dictionary, convertors)

def gen_terms(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    for defn, code_block in gen_many("termset.txt", dictionary.contract_set, convertors):
        yield defn, code_block

def gen_terms_index(dictionary: Dictionary) -> str:
    tmpl = fsys.get_template("termset_index.txt")

    return tmpl.render(utils=convertors, dictionary=dictionary)

def gen_func_index(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    return gen_one("func_index.txt", dictionary, convertors)

def gen_func_stubs(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    tmpl_set = {
        FunctionType.POF: fsys.get_template("func_stub_pof.txt"),
        FunctionType.STF: fsys.get_template("func_stub_stf.txt")
    }
    iterator = fsys.yield_funcset(dictionary, path_to_java_funcs)
    for defn, func_type, event_type, suffix in iterator:
        yield defn, func_type, event_type, suffix, tmpl_set[func_type].render(
            defn=defn,
            event_type=event_type,
            suffix=suffix,
            utils=convertors,
            )

def gen_func_stubs_index(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    for defn, code_block in gen_many("func_stub_index.txt", dictionary.contract_set, convertors):
        yield defn, code_block

def gen_func_stubs_main(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    for defn, code_block in gen_many("func_stub_main.txt", dictionary.contract_set, convertors):
        yield defn, code_block
