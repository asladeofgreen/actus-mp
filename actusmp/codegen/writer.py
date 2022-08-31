import pathlib

from actusmp.codegen import convertor
from actusmp.codegen import generator
from actusmp.codegen.enums import TargetGenerator
from actusmp.codegen.enums import TargetLanguage
from actusmp.dictionary import get_dictionary
from actusmp.utils import fsys


def write(lang: TargetLanguage, dest: pathlib.Path, path_to_java_impl: pathlib.Path):
    """Writes to file system a set of code blocks to initialise an upstream library.

    :param lang: Target progamming language.
    :param dest: Path to directory to which code will be emitted.
    :param path_to_java_impl: Path to actus-code Java library from which funcs will be derived.
    
    """
    assert lang in TargetLanguage
    assert dest.exists and dest.is_dir
    assert path_to_java_impl.exists() and path_to_java_impl.is_dir()

    dictionary = get_dictionary()
    for typeof in TargetGenerator:
        ctx = generator.GeneratorContext(lang, typeof, dictionary, path_to_java_impl)
        for code_block, entity in generator.generate(ctx):
            code_dest = _get_path_to_code_dest(dest, ctx, entity)
            fsys.write(code_dest, code_block)


def _get_path_to_code_dest(dest: pathlib.Path, ctx: generator.GeneratorContext, entity):
    """Returns file system location to which code block will be written.
    
    """
    if ctx.typeof in (TargetGenerator.FuncStubPOF, TargetGenerator.FuncStubSTF):
        return _get_path_to_code_dest_2(dest, ctx, entity)
    else:
        return _get_path_to_code_dest_1(dest, ctx, entity)


def _get_path_to_code_dest_1(dest: pathlib.Path, ctx: generator.GeneratorContext, entity):
    """Returns file system location to which code block will be written.
    
    """
    if ctx.lang == TargetLanguage.python:
        if ctx.typeof == TargetGenerator.Enum:
            return dest / "enums" / f"{convertor.to_underscore_case(entity.identifier)}.py"
        elif ctx.typeof == TargetGenerator.EnumIndex:
            return dest / "enums" / "__init__.py"
        elif ctx.typeof == TargetGenerator.FuncIndex:
            return dest / "funcs" / "__init__.py"
        elif ctx.typeof == TargetGenerator.FuncStubIndex:
            return dest / "funcs" / f"{entity.type_info.acronym.lower()}" / "__init__.py" 
        elif ctx.typeof == TargetGenerator.FuncStubMain:
            return dest / "funcs" / f"{entity.type_info.acronym.lower()}" / "main.py" 
        elif ctx.typeof == TargetGenerator.StateSpace:
            return dest / "core" / "states.py"
        elif ctx.typeof == TargetGenerator.Termset:
            return dest / "terms" / f"{convertor.to_underscore_case(entity.type_info.acronym.lower())}.py"
        elif ctx.typeof == TargetGenerator.TermsetIndex:
            return dest / "terms" / "__init__.py"            

    elif ctx.lang == TargetLanguage.typescript:
        if ctx.typeof == TargetGenerator.Enum:
            return dest / "enums" / f"{convertor.to_pascal_case(entity.identifier)}.ts"
        elif ctx.typeof == TargetGenerator.EnumIndex:
            return dest / "enums" / "index.ts"
        elif ctx.typeof == TargetGenerator.FuncIndex:
            return dest / "funcs" / "index.ts"
        elif ctx.typeof == TargetGenerator.FuncStubIndex:
            return dest / "funcs" / f"{entity.type_info.acronym.lower()}" / "index.ts" 
        elif ctx.typeof == TargetGenerator.FuncStubMain:
            return dest / "funcs" / f"{entity.type_info.acronym.lower()}" / "main.ts" 
        elif ctx.typeof == TargetGenerator.StateSpace:
            return dest / "core" / "states.ts"
        elif ctx.typeof == TargetGenerator.Termset:
            return dest / "terms" / f"{convertor.to_pascal_case(entity.type_info.acronym.lower())}.ts"
        elif ctx.typeof == TargetGenerator.TermsetIndex:
            return dest / "terms" / "index.ts"

    elif ctx.lang == TargetLanguage.rust:
        if ctx.typeof == TargetGenerator.Enum:
            return dest / "enums" / f"{convertor.to_underscore_case(entity.identifier)}.rs"
        elif ctx.typeof == TargetGenerator.EnumIndex:
            return dest / "enums" / "mod.rs"
        elif ctx.typeof == TargetGenerator.FuncIndex:
            return dest / "funcs" / "mod.rs"
        elif ctx.typeof == TargetGenerator.FuncStubIndex:
            return dest / "funcs" / f"{entity.type_info.acronym.lower()}" / "mod.rs" 
        elif ctx.typeof == TargetGenerator.FuncStubMain:
            return dest / "funcs" / f"{entity.type_info.acronym.lower()}" / "main.rs" 
        elif ctx.typeof == TargetGenerator.StateSpace:
            return dest / "core" / "states.rs"
        elif ctx.typeof == TargetGenerator.Termset:
            return dest / "terms" / f"{convertor.to_underscore_case(entity.type_info.acronym.lower())}.rs"
        elif ctx.typeof == TargetGenerator.TermsetIndex:
            return dest / "terms" / "mod.rs"            

def _get_path_to_code_dest_2(dest: pathlib.Path, ctx: generator.GeneratorContext, entity):
    """Returns file system location to which code block will be written.
    
    """
    (defn, f_type, event_type, suffix) = entity
    
    fname = f"{f_type.name.lower()}_{event_type}"
    fname = f"{fname}_{suffix}" if suffix else f"{fname}"
    outdir = dest / "funcs" / f"{defn.type_info.acronym.lower()}"

    if ctx.lang == TargetLanguage.python:
        return outdir / f"{fname}.py"
    elif ctx.lang == TargetLanguage.typescript:
        return outdir / f"{fname}.ts"
    elif ctx.lang == TargetLanguage.typescript:
        return outdir / f"{fname}.rs"
