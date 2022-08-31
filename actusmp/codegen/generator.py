import pathlib

from actusmp.codegen import convertor
from actusmp.codegen import enums
from actusmp.codegen.enums import TargetGenerator
from actusmp.codegen.enums import TargetLanguage
from actusmp.codegen.enums import LANG_TEMPLATE_SUBFOLDER
from actusmp.codegen.enums import GENERATOR_ACTUS_FN
from actusmp.model import Dictionary
from actusmp.model import FunctionType
from actusmp.model import IterableEntity
from actusmp.utils import fsys


class GeneratorContext():
    """Contextual information passed amongst the generator set.
    
    """
    def __init__(self, lang: TargetLanguage, typeof: TargetGenerator, dictionary: Dictionary, path_to_java_funcs: pathlib.Path):
        """Instance constructor.
        
        :param lang: Target programming language.
        :param typeof: Tager generator type.
        :param dictionary: Actus dictionary wrapper.
        :param path_to_java_funcs: Path to core Java implementation.

        """
        self.lang = lang
        self.typeof = typeof
        self.dictionary = dictionary
        self.path_to_java_funcs = path_to_java_funcs

def generate(ctx: GeneratorContext):
    """Returns code emitted by a generator.

    :param ctx: Generator contextual information.    
    :returns: A generated code block.

    """
    # Set template.
    tmpl = _get_template(ctx)

    # Set code block factory.
    if ctx.typeof in (TargetGenerator.FuncStubPOF, TargetGenerator.FuncStubSTF):
        factory = lambda: _gen_from_java_funcs(tmpl, ctx)
    else:
        entity = _get_entity(ctx)
        if entity == ctx.dictionary:
            factory = lambda: _gen_from_dictionary(tmpl, entity)
        else:
            factory = lambda: _gen_from_iterable_entity(tmpl, entity)

    # Yield 2 member tuple: (code block, domain entity).
    for entity, code_block in factory():
        yield code_block, entity

def _gen_from_dictionary(tmpl: pathlib.Path, dictionary: Dictionary):
    """Yields a single generated code block."""
    yield dictionary, tmpl.render(defn=dictionary, dictionary=dictionary, utils=convertor)

def _gen_from_iterable_entity(tmpl: pathlib.Path, definitions: IterableEntity):
    """Yields a set of generated code blocks."""
    for defn in definitions:
        yield defn, tmpl.render(defn=defn, utils=convertor)

def _gen_from_java_funcs(tmpl: pathlib.Path, ctx: GeneratorContext):
    """Returns generator yielding set of function stubs."""
    f_type = GENERATOR_ACTUS_FN[ctx.typeof]
    f_iterator = fsys.yield_funcset(ctx.dictionary, ctx.path_to_java_funcs, f_type)
    for defn, event_type, suffix in f_iterator:
        yield (defn, f_type, event_type, suffix), \
              tmpl.render(defn=defn, event_type=event_type, suffix=suffix, utils=convertor)

def _get_entity(ctx: GeneratorContext):
    """Returns entity against which generation will execute.
    
    """
    if ctx.typeof == TargetGenerator.Enum:
        return ctx.dictionary.enum_set
    elif ctx.typeof in (
        TargetGenerator.FuncStubIndex,
        TargetGenerator.FuncStubMain,
        TargetGenerator.FuncStubPOF,
        TargetGenerator.FuncStubSTF,
        TargetGenerator.Termset,
        ):
        return ctx.dictionary.contract_set
    
    return ctx.dictionary


def _get_template(ctx: GeneratorContext):
    """Returns template over which generation will execute.
    
    """
    dirname = LANG_TEMPLATE_SUBFOLDER[ctx.lang]
    filename = convertor.to_underscore_case(ctx.typeof.name).lower()

    return fsys.get_template(f"{dirname}_{filename}.txt")
