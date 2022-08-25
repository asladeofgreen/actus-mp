import typing

from actusmp.codegen.enums import TargetGenerator
from actusmp.codegen.enums import TargetLanguage
from actusmp.codegen.py import convertors as convertor_py
from actusmp.codegen.ts import convertor as convertor_ts
from actusmp.model import Dictionary
from actusmp.utils.convertors import to_underscore_case
from actusmp.utils.generators import gen_many
from actusmp.utils.generators import gen_one


# Map: TargetLanguage <-> template subfolder name.
_LANG_TEMPLATE_SUBFOLDER: typing.Map = {
    TargetLanguage.python: "py",
    TargetLanguage.rust: "rs",
    TargetLanguage.typescript: "ts",
}

# Map: TargetLanguage <-> template subfolder name.
_LANG_CONVERTOR = {
    TargetLanguage.python: convertor_py,
    TargetLanguage.rust: None,
    TargetLanguage.typescript: convertor_ts,
}

def generate(lang: TargetLanguage, generator_type: TargetGenerator, dictionary: Dictionary):
    convertor = _LANG_CONVERTOR[lang]
    entity = _get_entity(lang, generator_type, dictionary)
    template = _get_template(lang, generator_type)

    if entity == dictionary:
        yield entity, gen_one(template, entity, convertor)
    else:
        for entity, code_block in gen_many(template, entity, convertor):
            yield entity, code_block


def _get_entity(lang: TargetLanguage, generator_type: TargetGenerator, dictionary: Dictionary):
    if generator_type == TargetGenerator.Enum:
        return dictionary.enum_set
    elif generator_type in (
        TargetGenerator.FuncStubIndex,
        TargetGenerator.FuncStubMain,
        TargetGenerator.Termset,
        ):
        return dictionary.contract_set
    
    return dictionary

def _get_template(lang: TargetLanguage, generator_type: TargetGenerator):
    dirname = _LANG_TEMPLATE_SUBFOLDER[lang]
    filename = to_underscore_case(generator_type.name).lower()

    return f"{dirname}/{filename}.txt" 


# def _gen_enums(dictionary: Dictionary) -> typing.Tuple[Term, str]:
#     for defn, code_block in gen_many("enum.txt", dictionary.enum_set, convertors):
#         yield defn, code_block

# def _gen_enums_index(dictionary: Dictionary) -> str:
#     return gen_one("enum_index.txt", dictionary, convertors)

# def _gen_state_space(dictionary: Dictionary) -> str:
#     return gen_one("state_space.txt", dictionary, convertors)

# def _gen_terms(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
#     for defn, code_block in gen_many("termset.txt", dictionary.contract_set, convertors):
#         yield defn, code_block

# def _gen_terms_index(dictionary: Dictionary) -> str:
#     return gen_one("termset_index.txt", dictionary, convertors)

# def _gen_func_index(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
#     return gen_one("func_index.txt", dictionary, convertors)

# def _gen_func_stub_index(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
#     for defn, code_block in gen_many("func_stub_index.txt", dictionary.contract_set, convertors):
#         yield defn, code_block

# def _gen_func_stub_main(dictionary: Dictionary) -> typing.Tuple[Contract, str]:
#     for defn, code_block in gen_many("func_stub_main.txt", dictionary.contract_set, convertors):
#         yield defn, code_block

# def _gen_func_stub_pof(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
#     tmpl_set = {
#         FunctionType.POF: fsys.get_template("func_stub_pof.txt"),
#         FunctionType.STF: fsys.get_template("func_stub_stf.txt")
#     }
#     iterator = fsys.yield_funcset(dictionary, path_to_java_funcs)
#     for defn, func_type, event_type, suffix in iterator:
#         yield defn, func_type, event_type, suffix, tmpl_set[func_type].render(
#             defn=defn,
#             event_type=event_type,
#             suffix=suffix,
#             utils=convertors,
#             )

# def _gen_func_stub_stf(dictionary: Dictionary, path_to_java_funcs: pathlib.Path) -> typing.Tuple[Contract, str]:
#     tmpl_set = {
#         FunctionType.POF: fsys.get_template("func_stub_pof.txt"),
#         FunctionType.STF: fsys.get_template("func_stub_stf.txt")
#     }
#     iterator = fsys.yield_funcset(dictionary, path_to_java_funcs)
#     for defn, func_type, event_type, suffix in iterator:
#         yield defn, func_type, event_type, suffix, tmpl_set[func_type].render(
#             defn=defn,
#             event_type=event_type,
#             suffix=suffix,
#             utils=convertors,
#             )
