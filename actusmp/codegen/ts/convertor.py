from actusmp.model import Enum
from actusmp.model import EnumMember
from actusmp.model import ScalarType
from actusmp.model import Term
from actusmp.utils.convertors import *


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
            except:
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
    except:
        raise

    try:
        int(member_name[0])
    except ValueError:
        return member_name
    else:
        return f"_{member_name}"
