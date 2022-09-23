import typing

from actusmp.dictionary.accessor import Accessor
from actusmp.model import ApplicableTermInfoSet
from actusmp.model import ApplicableTermInfo
from actusmp.model import Contract
from actusmp.model import ContractSet
from actusmp.model import Dictionary
from actusmp.model import Enum
from actusmp.model import EnumMember
from actusmp.model import ContractTypeInfo
from actusmp.model import ContractTypePublicationStatus
from actusmp.model import ScalarType
from actusmp.model import State
from actusmp.model import StateSet
from actusmp.model import Taxonomy
from actusmp.model import Term
from actusmp.model import TermSet


def get_dictionary() -> Dictionary:
    """Maps actus-dictionary.json file -> meta model.

    """
    accessor = Accessor()
    applicability = _get_applicability(accessor)
    taxonomy = _get_taxonomy(accessor)
    term_set = _get_term_set(accessor)

    return Dictionary(
        applicability=applicability,
        contract_event_type=_get_enum(accessor.contract_event_type),
        contract_performance=_get_enum(accessor.contract_performance),
        contract_role=_get_enum(accessor.contract_role),
        contract_reference_role=_get_enum(accessor.contract_reference_role),
        contract_reference_type=_get_enum(accessor.contract_reference_type),
        contract_type=_get_enum(accessor.contract_type),
        contract_set=_get_contract_set(applicability, taxonomy, term_set),
        state_set=_get_state_set(accessor),
        taxonomy=taxonomy,
        term_set=term_set,
        version=accessor.version,
        version_date=accessor.version_date
        )


def _get_applicability(accessor: Accessor) -> ApplicableTermInfoSet:
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

    return ApplicableTermInfoSet(items)


def _get_contract_set(
    applicability: ApplicableTermInfoSet,
    taxonomy: Taxonomy,
    term_set: TermSet
) -> ContractSet:
    """Decodes set of derived contract declarations.

    """
    def _map_termset(type_info: ContractTypeInfo) -> TermSet:
        contract_termset = []
        for applicable_term_info in applicability.get_applicable_termset(type_info):
            contract_termset.append(term_set.get_term(applicable_term_info.term_id))

        return TermSet(contract_termset)

    def _map_contract(type_info: ContractTypeInfo) -> Contract:
        return Contract(
            term_set=_map_termset(type_info),
            type_info=type_info,
        )

    return ContractSet(
        [i for i in map(lambda i: _map_contract(i), taxonomy) if i.type_info.acronym != "EXOTi"]
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
            return _get_enum_member(value)
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
        scalar_type = ScalarType[obj.get("type", "Unknown")]

        return State(
            acronym=obj["acronym"],
            allowed_values=[_map_allowed_value(scalar_type, i) for i in obj["allowedValues"]],
            description=obj["description"],
            identifier=obj["identifier"],
            is_array=False,
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
            publication_status=ContractTypePublicationStatus[obj.get("status", "Unknown")]
        )

    return Taxonomy([_map_contract_type_info(i) for i in accessor.taxonomy])


def _get_term_set(accessor: Accessor) -> TermSet:
    """Decodes set of terms from Actus dictionary.

    """
    def _map_default(is_array: bool, scalar_type: ScalarType, value: str):
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

    def _map_allowed(
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
        else:
            return value

    def _map_term(obj: dict) -> Term:
        is_array: bool = obj["type"].endswith("[]")
        scalar_type_raw = obj["type"] if not is_array else obj["type"][:-2]
        scalar_type = ScalarType[scalar_type_raw]
        default_value = _map_default(is_array, scalar_type, obj["default"])
        allowed = [_map_allowed(scalar_type, i, default_value) for i in obj["allowedValues"]]

        return Term(
            acronym=obj["acronym"],
            allowed_values=allowed,
            default=default_value,
            description=obj.get("description", obj["name"]).replace("\n", ""),
            group_id=obj["group"],
            identifier=obj["identifier"],
            is_array=is_array,
            name=obj['name'],
            scalar_type=scalar_type
        )

    return TermSet([_map_term(i) for i in accessor.term_set])
