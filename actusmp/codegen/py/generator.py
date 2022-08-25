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


def gen_funcset_stubs_1(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    tmpl_set = {
        FunctionType.POF: fsys.get_template("funcset/stub_pof.txt"),
        FunctionType.STF: fsys.get_template("funcset/stub_stf.txt")
    }

    iterator = fsys.yield_funcset(dictionary, path_to_java_funcs)
    for contract, func_type, event_type, suffix in iterator:
        code_block = tmpl_set[func_type].render(utils=convertors, contract=contract, event_type=event_type, suffix=suffix)
        yield contract, func_type, event_type, suffix, code_block


def gen_funcset_stubs_2(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    tmpl = fsys.get_template("funcset/stub_main.txt")

    for contract in dictionary.contract_set:
        code_block = tmpl.render(utils=convertors, contract=contract)
        yield contract, code_block


def gen_funcset_stubs_pkg_init(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    tmpl = fsys.get_template("funcset/stub_pkg_init.txt")

    for contract in dictionary.contract_set:
        funcset_iterator = fsys.yield_funcset(dictionary, path_to_java_funcs, contract)
        code_block = tmpl.render(utils=convertors, contract=contract, funcset_iterator=funcset_iterator)
        if len(code_block) > 0:
            yield contract, code_block

# def gen_typeset_pkg_init(dictionary: Dictionary) -> str:
#     tmpl = fsys.get_template("typeset/pkg_init.txt")

#     return tmpl.render(utils=convertors, dictionary=dictionary)

