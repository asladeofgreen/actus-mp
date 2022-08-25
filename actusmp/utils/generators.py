import typing

from actusmp.model import Dictionary
from actusmp.model import IterableEntity
from actusmp.utils import fsys


def gen_many(tmpl: str, definitions: IterableEntity, convertor: typing.Callable):
    tmpl = fsys.get_template(tmpl)
    for defn in definitions:
        yield defn, tmpl.render(defn=defn, utils=convertor)

def gen_one(tmpl: str, dictionary: Dictionary, convertor: typing.Callable):
    return fsys.get_template(tmpl).render(dictionary=dictionary, utils=convertor)

