from actusmp.model import Enum
from actusmp.model import EnumMember
from actusmp.model import ScalarType
from actusmp.model import Term
from actusmp.utils.convertors import *


def to_js_type(term: Term) -> str:
    """Maps an Actus term's type to it's js equivalent.
    
    """
    def _map(typedef: ScalarType):
        if typedef == ScalarType.ContractReference:
            return "contracts.ContractReference"
        elif typedef == ScalarType.Cycle:
            return "auxiliary.Cycle"
        elif typedef == ScalarType.Enum:
            return f"enums.{to_camel_case(term.identifier)}"
        elif typedef == ScalarType.Period:
            return "auxiliary.Period"
        elif typedef == ScalarType.Real:
            return "number"
        elif typedef == ScalarType.Timestamp:
            return "Date"
        elif typedef == ScalarType.Varchar:
            return "string"
        else:
            raise ValueError(f"Unsupported term scalar type: {term.scalar_type} :: {typedef}")        

    if term.is_array:
        return f"typing.List[{_map(term.scalar_type)}]"
    else:
        return _map(term.scalar_type)


def to_js_default(term: Term) -> str:
    """Maps an Actus term's default value to it's js equivalent.
    
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
            except:
                return float(0)

        return f"'TODO: format {term.scalar_type} :: {term.default}'"


def to_js_enum_member(definition: Enum, member: EnumMember) -> str:
    """Maps an enum member to a python safe enum member name.
    
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
