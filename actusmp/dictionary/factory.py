import typing

from actusmp.dictionary.accessor import Accessor
from actusmp.model import Applicability
from actusmp.model import ApplicableContractTermInfo
from actusmp.model import Contract
from actusmp.model import ContractSet
from actusmp.model import Dictionary
from actusmp.model import Enum
# from actusmp.model import EnumMember
# from actusmp.model import State
# from actusmp.model import StateSet

from actusmp.model1 import Applicability
from actusmp.model1 import ApplicableTermInfo
from actusmp.model1 import Contract
from actusmp.model1 import ContractSet
from actusmp.model1 import ContractTerm
from actusmp.model1 import Dictionary
from actusmp.model1 import Enum
from actusmp.model1 import EnumMember
from actusmp.model1 import ContractTypeInfo
from actusmp.model1 import PublicationStatus
from actusmp.model1 import ScalarType
from actusmp.model1 import State
from actusmp.model1 import StateSet
from actusmp.model1 import Taxonomy
from actusmp.model1 import Term
from actusmp.model1 import TermSet


def get_dictionary() -> Dictionary:
    """Maps actus-dictionary.json file -> meta model.
    
    """
    accessor = Accessor()
    applicability=_get_applicability(accessor)
    taxonomy=_get_taxonomy(accessor)
    term_set=_get_term_set(accessor)

    contract_set = _get_contract_set(accessor, applicability, taxonomy, term_set)

    return Dictionary(
        applicability=applicability,
        contract_event_type=_get_enum(accessor.contract_event_type),
        contract_reference_role=_get_enum(accessor.contract_reference_role),
        contract_reference_type=_get_enum(accessor.contract_reference_type),
        state_set=_get_state_set(accessor),
        taxonomy=taxonomy,
        term_set=term_set,
        version=accessor.version,
        version_date=accessor.version_date
        )

    applicability=_get_applicability(accessor)
    global_term_set = _get_term_set(accessor)

    return Dictionary(
        applicability=applicability,
        contract_reference_enum_set=_contract_reference_enum_set(accessor),
        contract_set=_get_contract_set(accessor, global_term_set, applicability),
        global_term_set=global_term_set,
        state_set=_get_state_set(accessor),
        version=accessor.version,
        version_date=accessor.version_date
    )


def _get_applicability(accessor: Accessor) -> Applicability:
    """Decodes applicability declarations.
    
    """    
    items = []
    for contract_id, applicable_terms in accessor.applicability:
        for term_id, term_instruction in applicable_terms.items():
            if term_id == "contract":
                continue            
            items.append(
                ApplicableTermInfo(
                    contract_type_id=contract_id,
                    term_id=term_id,
                    term_instruction=term_instruction
                )
            )

    return Applicability(items)


def _get_contract_set(
    accessor: Accessor,
    applicability: Applicability,
    taxonomy: Taxonomy,
    term_set: TermSet
    ) -> ContractSet:
    """Decodes set of derived contract declarations.
    
    """
    def _map_contract_termset(contract_type_info: ContractTypeInfo) -> Contract:
        termset = []
        for applicable_term_info in applicability.get_applicable_termset(contract_type_info):
            term_defn = term_set.get_term(applicable_term_info.term_id)
            termset.append(ContractTerm(
                    acronym=term_defn.acronym,
                    allowed_values=term_defn.allowed_values,
                    default=term_defn.default,
                    description=term_defn.description,
                    group_id=term_defn.group_id,
                    identifier=term_defn.identifier,
                    is_array=term_defn.is_array,
                    name=term_defn.name,
                    scalar_type=term_defn.scalar_type
                ))
        
        return termset

    def _map_contract(contract_type_info: ContractTypeInfo) -> Contract:
        return Contract(
            term_set=_map_contract_termset(contract_type_info),
            type_info=contract_type_info,
        )

    return ContractSet(
        list(map(lambda i: _map_contract(i), taxonomy))
        )


def _get_enum(obj: dict) -> EnumMember:
    """Decodes an enumeration declaration.
    
    """
    return Enum(
        acronym=obj["acronym"],
        description=obj["description"],
        identifier=obj["identifier"],
        members=[_get_enum_member(i) for i in obj["allowedValues"]],
        name=obj["name"],
    )


def _get_enum_member(obj: dict, is_default: typing.Optional[bool] = None) -> EnumMember:
    """Decodes an enumeration member declaration.
    
    """
    return EnumMember(
        acronym=obj["acronym"],
        description=obj["description"],
        identifier=obj["identifier"],
        is_default=is_default,
        name=obj["name"],
        option=int(obj["option"]),
    )


def _get_state_set(accessor: Accessor) -> StateSet:
    """Decodes set of states from Actus dictionary.
    
    """
    def _map_allowed_value(scalar_type: ScalarType, value: typing.Union[str, dict]):
        if scalar_type == ScalarType.Enum:
            return EnumMember(
                acronym=value["acronym"],
                description=value["description"],
                identifier=value["identifier"],
                is_default=None,
                name=value["name"],
                option=value["option"]
            )
        return value

    def _map_state(obj: dict) -> State:
        scalar_type=ScalarType[obj.get("type", "Unknown")]

        return State(
            acronym=obj["acronym"],
            allowed_values=[_map_allowed_value(scalar_type, i) for i in obj["allowedValues"]],
            description=obj["description"],
            identifier=obj["identifier"],
            name=obj["name"],
            scalar_type=scalar_type
        )

    return StateSet([_map_state(i) for i in accessor.state_set])


def _get_taxonomy(accessor: Accessor) -> Taxonomy:
    """Decodes taxonomy information from Actus dictionary.
    
    """
    def _map_contract_type_info(obj: dict) -> ContractTypeInfo:
        return ContractTypeInfo(
            acronym=obj["acronym"],
            classification=obj["class"],
            coverage=obj.get("coverage"),
            description=obj["description"],
            family=obj["family"],
            identifier=obj["identifier"],
            name=obj["name"],
            publication_status=PublicationStatus[obj.get("status", "Unknown")]
        )

    return Taxonomy([_map_contract_type_info(i) for i in accessor.taxonomy])


def _get_term_set(accessor: Accessor) -> TermSet:
    """Decodes set of terms from Actus dictionary.
    
    """
    def _map_default_value(
        is_array: bool,
        scalar_type: ScalarType,
        value: str
        ):
        if value is None:
            return [] if is_array else None
        elif scalar_type == ScalarType.Enum:
            return value.upper()
        elif scalar_type == ScalarType.Real:
            try:
                return float(value)
            except ValueError:
                pass
        else:
            print(f"TODO: map default value: {is_array} {scalar_type} {value}")
            return value

    def _map_allowed_value(
        scalar_type: ScalarType,
        value: typing.Union[str, dict],
        default: typing.Union[str, float, list]
        ):
        if scalar_type == ScalarType.Enum:
            return EnumMember(
                acronym=value["acronym"],
                description=value["description"],
                identifier=value["identifier"],
                is_default=value["acronym"] == default,
                name=value["name"],
                option=value["option"]
            )
        return value

    def _map_term(obj: dict) -> Term:
        is_array: bool = obj["type"].endswith("[]")
        scalar_type_raw = obj["type"] if not is_array else obj["type"][:-2]
        scalar_type=ScalarType[scalar_type_raw]
        default_value=_map_default_value(is_array, scalar_type, obj["default"])

        return Term(
            acronym=obj["acronym"],
            allowed_values=[_map_allowed_value(scalar_type, i, default_value) for i in obj["allowedValues"]],
            default=default_value,
            description=obj.get("description", obj["name"]).replace("\n", ""),
            group_id=obj["group"],
            identifier=obj["identifier"],
            is_array=is_array,
            name=obj['name'],
            scalar_type=obj["type"]
        )

    return TermSet([_map_term(i) for i in accessor.term_set])



#################################
# Obsolete
#################################

def _get_term(obj: dict, prefix: str = "") -> Term:
    if obj["type"].startswith("Enum"):
        return Enum(
            _members=[_get_enum_member(obj["identifier"], i) for i in obj["allowedValues"]],
            acronym=obj["acronym"],
            allowed_values=obj["allowedValues"],
            default=obj.get("default"),
            description=obj.get("description", obj["name"]).replace("\n", ""),
            group_id=obj.get("group"),
            identifier=f"{prefix}{obj['identifier']}",
            name=obj['name'],
            type=obj["type"]
        )
    else:
        return Term(
            acronym=obj["acronym"],
            allowed_values=obj["allowedValues"],
            default=obj["default"],
            description=obj.get("description", obj["name"]).replace("\n", ""),
            group_id=obj["group"],
            identifier=obj["identifier"],
            name=obj['name'],
            scalar_type=obj["type"]
        )

def _get_contract(obj: dict, global_term_set: TermSet, applicability: Applicability) -> Contract:
    return Contract(
        acronym=obj["acronym"],
        classification=obj["class"],
        identifier=obj["identifier"],
        coverage=obj.get("coverage"),
        description=obj["description"],
        family=obj["family"],
        name=obj["name"],
        status=obj.get("status", "Unknown"),
        term_set=_get_contract_term_set(obj["identifier"], global_term_set, applicability)
    )


def _get_contract_term_set(contract_id: str, applicability: Applicability, term_set: TermSet) -> Contract:
    print(contract_id)

    contract_term_set = []
    for info in applicability.get_applicable_termset(contract_id):
        for term in term_set:
            if term.identifier == info.term_id:
                contract_term_set.append(term)

    return TermSet(contract_term_set)
