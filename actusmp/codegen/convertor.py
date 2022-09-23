import re

from actusmp.model import Enum
from actusmp.model import EnumMember
from actusmp.model import ScalarType
from actusmp.model import Term


def to_camel_case(name: str, separator: str = '_'):
    """Converts passed name to camel case.

    :param name: A name as specified in ontology specification.
    :param separator: Separator to use in order to split name into constituent parts.
    :returns: A string converted to camel case.

    """
    r = ''
    if name is not None:
        s = name.split(separator)
        for s in s:
            if (len(s) > 0):
                r += s[0].upper()
                if (len(s) > 1):
                    r += s[1:]
    return r


def to_pascal_case(name: str, separator: str = '_'):
    """Converts passed name to pascal case.

    :param name: A name as specified in ontology specification.
    :param separator: Separator to use in order to split name into constituent parts.
    :returns: A string converted to pascal case.

    """
    r = ''
    s = to_camel_case(name, separator)
    if (len(s) > 0):
        r += s[0].lower()
        if (len(s) > 1):
            r += s[1:]
    return r


def to_py_type(term: Term) -> str:
    """Maps an Actus term's type to it's pythonic equivalent.

    """
    def _map(typedef: ScalarType):
        if typedef == ScalarType.ContractReference:
            return "core.ContractReference"
        elif typedef == ScalarType.Cycle:
            return "core.Cycle"
        elif typedef == ScalarType.Enum:
            return f"enums.{to_camel_case(term.identifier)}"
        elif typedef == ScalarType.Period:
            return "core.Period"
        elif typedef == ScalarType.Real:
            return "float"
        elif typedef == ScalarType.Timestamp:
            return "datetime.datetime"
        elif typedef == ScalarType.Varchar:
            return "str"
        else:
            raise ValueError(f"Unsupported term scalar type: {term.scalar_type} :: {typedef}")

    if term.is_array:
        return f"typing.List[{_map(term.scalar_type)}]"
    else:
        return _map(term.scalar_type)


def to_py_default(term: Term) -> str:
    """Maps an Actus term's default value to it's pythonic equivalent.

    """
    def get_enum_default_acronym():
        for member in term.allowed_values:
            if member.is_match(term.default):
                return member.acronym
        print(f"WARNING: enum member default is incorrect, reverting to option 0 :: {term}")
        return term.allowed_values[0].acronym

    if term.default:
        if term.scalar_type == ScalarType.Enum:
            return f"enums.{to_camel_case(term.identifier)}.{get_enum_default_acronym()}"
        elif term.scalar_type == ScalarType.Period:
            return "None"
        elif term.scalar_type == ScalarType.Real:
            try:
                return float(term.default)
            except ValueError:
                return float(0)

        return f"'TODO: format {term.scalar_type} :: {term.default}'"


def to_py_enum_member(definition: Enum, member: EnumMember) -> str:
    """Maps an enum member to a python safe enum member name.

    """
    # Some enum members begin with an integer which is unsafe in python.
    member_name = member.acronym
    try:
        member_name = member_name.upper()
    except BaseException:
        raise

    try:
        int(member_name[0])
    except ValueError:
        return member_name
    else:
        return f"_{member_name}"


def to_rs_type(term: Term) -> str:
    """Maps an Actus term's type to it's rusty equivalent.

    """
    def _map(typedef: ScalarType):
        if typedef == ScalarType.ContractReference:
            return "core::ContractReference"
        elif typedef == ScalarType.Cycle:
            return "core::Cycle"
        elif typedef == ScalarType.Enum:
            return f"enums::{to_camel_case(term.identifier)}"
        elif typedef == ScalarType.Period:
            return "core::Period"
        elif typedef == ScalarType.Real:
            return "f64"
        elif typedef == ScalarType.Timestamp:
            return "core::Timestamp"
            return "datetime.datetime"
        elif typedef == ScalarType.Varchar:
            return "String"
        else:
            raise ValueError(f"Unsupported term scalar type: {term.scalar_type} :: {typedef}")

    if term.is_array:
        return f"Vec<{_map(term.scalar_type)}>"
    else:
        return _map(term.scalar_type)


def to_rs_default(term: Term) -> str:
    """Maps an Actus term's default value to it's rusty equivalent.

    """
    def get_enum_default_acronym():
        for member in term.allowed_values:
            if member.is_match(term.default):
                return member.acronym
        print(f"WARNING: enum member default is incorrect, reverting to option 0 :: {term}")
        return term.allowed_values[0].acronym

    if term.default:
        if term.scalar_type == ScalarType.Enum:
            return f"enums.{to_camel_case(term.identifier)}.{get_enum_default_acronym()}"
        elif term.scalar_type == ScalarType.Period:
            return "None"
        elif term.scalar_type == ScalarType.Real:
            try:
                return float(term.default)
            except ValueError:
                return float(0)

        return f"'TODO: format {term.scalar_type} :: {term.default}'"


def to_rs_enum_member(definition: Enum, member: EnumMember) -> str:
    """Maps an enum member to a rusty safe enum member name.

    """
    # Some enum members begin with an integer which is unsafe in python.
    member_name = member.acronym
    try:
        member_name = member_name.upper()
    except BaseException:
        raise

    try:
        int(member_name[0])
    except ValueError:
        return member_name
    else:
        return f"_{member_name}"


def to_ts_type(term: Term) -> str:
    """Maps an Actus term's type to it's typescript equivalent.

    """
    def _map(typedef: ScalarType):
        if typedef == ScalarType.ContractReference:
            return "core.ContractReference"
        elif typedef == ScalarType.Cycle:
            return "core.Cycle"
        elif typedef == ScalarType.Enum:
            return f"enums.{to_camel_case(term.identifier)}"
        elif typedef == ScalarType.Period:
            return "core.Period"
        elif typedef == ScalarType.Real:
            return "number"
        elif typedef == ScalarType.Timestamp:
            return "Date"
        elif typedef == ScalarType.Varchar:
            return "string"
        else:
            raise ValueError(f"Unsupported term scalar type: {term.scalar_type} :: {typedef}")

    if term.is_array:
        return f"Array<{_map(term.scalar_type)}>"
    else:
        return _map(term.scalar_type)


def to_ts_default(term: Term) -> str:
    """Maps an Actus term's default value to it's typescript equivalent.

    """
    def get_enum_default_acronym():
        for member in term.allowed_values:
            if member.is_match(term.default):
                return member.acronym
        print(f"WARNING: enum member default is incorrect, reverting to option 0 :: {term}")
        return term.allowed_values[0].acronym

    if term.is_array:
        return "[]"

    elif term.default:
        if term.scalar_type == ScalarType.Cycle:
            return ""
        elif term.scalar_type == ScalarType.Enum:
            return f"enums.{to_camel_case(term.identifier)}.{get_enum_default_acronym()}"
        elif term.scalar_type == ScalarType.Period:
            return ""
        elif term.scalar_type == ScalarType.Real:
            try:
                return float(term.default)
            except ValueError:
                return float(0)
        else:
            return f"'TODO: format default {term.scalar_type} :: {term.default}'"

    elif term.scalar_type == ScalarType.Real:
        return float(0)

    return "null"


def to_ts_optional_flag(term: Term) -> str:
    """Maps an Actus term to it's typescript optionality flag.

    """
    return "" if term.default else "?"


def to_ts_enum_member(member: EnumMember) -> str:
    """Maps an enum member to a typescript safe enum member name.

    """
    # Some enum members begin with an integer which is unsafe in js.
    member_name = member.acronym
    try:
        member_name = member_name.upper()
    except BaseException:
        raise

    try:
        int(member_name[0])
    except ValueError:
        return member_name
    else:
        return f"_{member_name}"


def to_underscore_case(target: str):
    """Helper function to convert a from camel case string to an underscore case string.

    :param target: A string for conversion.
    :returns: A string converted to underscore case, e.g. account_number.

    """
    if target is None or not len(target):
        return ''

    r = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', target)
    r = re.sub('([a-z0-9])([A-Z])', r'\1_\2', r)
    r = r.lower()

    return r
