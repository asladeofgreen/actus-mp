import pathlib
import typing

from actusmp.model import Contract
from actusmp.model import Dictionary
from actusmp.model import IterableEntity
from actusmp.model import FunctionType
from actusmp.codegen.ts import convertor
from actusmp.utils import fsys


def gen_enums(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    for defn, code_block in _gen_many("enum.txt", dictionary.enum_set):
        yield defn, code_block

def gen_enums_index(dictionary: Dictionary) -> str:
    return _gen_one("enum_index.txt",dictionary)

def gen_funcs_index(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    return _gen_one("func_index.txt",dictionary)

def gen_funcs_stubs(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
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
            utils=convertor,
            )

def gen_funcs_stubs_index(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
    for defn, code_block in _gen_many("func_stub_index.txt", dictionary.contract_set):
        yield defn, code_block

def gen_funcs_stubs_main(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    for defn, code_block in _gen_many("func_stub_main.txt", dictionary.contract_set):
        yield defn, code_block

def gen_state_space(dictionary: Dictionary) -> str:
    return _gen_one("state_space.txt",dictionary)

def gen_termsets(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
    for defn, code_block in _gen_many("termset.txt", dictionary.contract_set):
        yield defn, code_block

def gen_termsets_index(dictionary: Dictionary) -> str:
    return _gen_one("termset_index.txt",dictionary)

def _gen_many(tmpl: str, definitions: IterableEntity):
    tmpl = fsys.get_template(tmpl)
    for defn in definitions:
        yield defn, tmpl.render(defn=defn, utils=convertor)

def _gen_one(tmpl: str, dictionary: Dictionary):
    return fsys.get_template(tmpl).render(dictionary=dictionary, utils=convertor)
