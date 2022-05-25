from actusmp.dictionary.accessor import Accessor
from actusmp.model import Applicability
from actusmp.model import ApplicableContractTermInfo
from actusmp.model import Contract
from actusmp.model import ContractSet
from actusmp.model import Dictionary
from actusmp.model import Enum
from actusmp.model import EnumMember
from actusmp.model import State
from actusmp.model import StateSet
from actusmp.model import Term
from actusmp.model import TermSet


def get_dictionary() -> Dictionary:
    """Maps actus-dictionary.json file -> meta model.
    
    """
    accessor = Accessor()
    applicability=_get_applicability(accessor)
    global_term_set = _get_term_set(accessor)
    state_set = _get_state_set(accessor)

    return Dictionary(
        applicability=applicability,
        contract_set=_get_contract_set(accessor, global_term_set, applicability),
        global_term_set=global_term_set,
        state_set=state_set,
        version=accessor.version,
        version_date=accessor.version_date
    )


def _get_applicability(accessor: Accessor) -> Applicability:
    items = []
    for obj in accessor.applicability:
        contract_id = obj["contract"]
        for term_id, info in obj.items():
            if term_id == "contract":
                continue
            items.append(
                ApplicableContractTermInfo(
                    contract_id=contract_id,
                    term_id=term_id,
                    info=info
                )
            )

    return Applicability(items)


def _get_contract_set(accessor: Accessor, global_term_set: TermSet, applicability: Applicability) -> ContractSet:
    return ContractSet(
        list(map(lambda i: _get_contract(i, global_term_set, applicability), accessor.contract_type_set))
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


def _get_contract_term_set(contract_id: str, global_term_set: TermSet, applicability: Applicability) -> Contract:
    contract_term_set = []
    for applicability_item in applicability.get_set_by_contract_id(contract_id):
        for term in global_term_set:
            if term.identifier == applicability_item.term_id:
                contract_term_set.append(term)

    return TermSet(contract_term_set)


def _get_enum_member(obj: dict) -> EnumMember:
    return EnumMember(
        acronym=obj["acronym"],
        description=obj["description"],
        identifier=obj["identifier"],
        name=obj["name"],
        option=int(obj["option"]),
    )


def _get_state_set(accessor: Accessor) -> StateSet:
    return StateSet(list(map(_get_state, accessor.state_set)))


def _get_state(obj: dict) -> Term:
    if obj["type"].startswith("Enum"):
        return State(
            acronym=obj["acronym"],
            allowed_values=obj["allowedValues"],
            description=obj.get("description", obj["name"]),
            enum_members=[_get_enum_member(i) for i in obj["allowedValues"]],
            identifier=obj["identifier"],
            name=obj["name"],
            type=obj["type"]
        )
    else:
        return State(
            acronym=obj["acronym"],
            allowed_values=obj["allowedValues"],
            description=obj.get("description", obj["name"]),
            enum_members=[],
            identifier=obj["identifier"],
            name=obj["name"],
            type=obj["type"]
        )


def _get_term_set(accessor: Accessor) -> TermSet:
    return TermSet(list(map(_get_term, accessor.term_set)))


def _get_term(obj: dict) -> Term:
    if obj["type"].startswith("Enum"):
        return Enum(
            _members=[_get_enum_member(i) for i in obj["allowedValues"]],
            acronym=obj["acronym"],
            allowed_values=obj["allowedValues"],
            default=None if len(obj["default"].strip()) == 0 else obj["default"].strip(),
            description=obj.get("description", obj["name"]).replace("\n", ""),
            group_id=obj["group"],
            identifier=obj["identifier"],
            name=obj["name"],
            type=obj["type"]
        )
    else:
        return Term(
            acronym=obj["acronym"],
            allowed_values=obj["allowedValues"],
            default=None if len(obj["default"].strip()) == 0 else obj["default"].strip(),
            description=obj.get("description", obj["name"]).replace("\n", ""),
            group_id=obj["group"],
            identifier=obj["identifier"],
            name=obj["name"],
            type=obj["type"]
        )
