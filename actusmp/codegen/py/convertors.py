from actusmp.model import EnumMember
from actusmp.model import Term
from actusmp.utils.convertors import *


def to_python_type(term: Term) -> str:
    """Maps an Actus term's type to it's pythonic equivalent.
    
    """
    def _map(typedef: str):
        if typedef == "ContractReference":
            return "auxiliary.ContractReference"
        elif typedef == "Cycle":
            return "auxiliary.Cycle"
        elif typedef == "Enum":
            return f"enums.{to_camel_case(term.identifier)}"
        elif typedef == "Period":
            return "auxiliary.Period"
        elif typedef == "Real":
            return "float"
        elif typedef == "Timestamp":
            return "datetime.datetime"
        elif typedef == "Varchar":
            return "str"
        else:
            raise ValueError(f"Unsupported term type: {term.type}")        

    if term.type.endswith("[]"):
        return f"typing.List[{_map(term.type[:-2])}]"
    else:
        return _map(term.type)


def to_python_default(term: Term) -> str:
    """Maps an Actus term's default value to it's pythonic equivalent.
    
    """
    if term.default:
        if term.type == "Enum":
            return f"enums.{to_camel_case(term.identifier)}.{to_python_enum_member_1(term.default_member)}"
        elif term.type == "Period":
            return "None"
        return f"'TODO: format {term.default}'"


def to_python_enum_member(member_name: str) -> str:
    """Maps an enum member name to a python safe enum member name.
    
    """
    # Some enum members begin with an integer which is unsafe in python.
    member_name = member_name.upper()
    try:
        int(member_name[0])
    except ValueError:
        return member_name
    else:
        return f"_{member_name}"


def to_python_enum_member_1(member: EnumMember) -> str:
    """Maps an enum member name to a python safe enum member name.
    
    """
    try:
        int(member.acronym[0])
    except ValueError:
        return member.acronym
    else:
        return f"_{member.acronym}"
