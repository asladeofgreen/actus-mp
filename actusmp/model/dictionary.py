import dataclasses
import datetime
import typing

from actusmp.model.applicability import ApplicableTermInfoSet
from actusmp.model.contract import ContractSet
from actusmp.model.enum_ import Enum
from actusmp.model.state import StateSet
from actusmp.model.taxonomy import Taxonomy
from actusmp.model.term import TermSet


@dataclasses.dataclass
class Dictionary():
    """An information set by which the ACTUS standard is declared.

    """
    # Criteria that determine which set of terms are associated with which type of contract.
    applicability: ApplicableTermInfoSet

    # Enumeration over set of contract event types.
    contract_event_type: Enum

    # Enumeration over set of contract performance status.
    contract_performance: Enum

    # Enumeration over set of contract roles.
    contract_role: Enum

    # Enumeration over set of intra-contract reference information.
    contract_reference_role: Enum

    # Enumeration over set of intra-contract reference types.
    contract_reference_type: Enum

    # Set of supported financial contracts.
    contract_set: ContractSet

    # Enumeration over set of contract types.
    contract_type: Enum

    # Set of states through which a contract may pass during it's lifetime.
    state_set: StateSet

    # Declaration of supported contract types.
    taxonomy: Taxonomy

    # Set of declared contract terms.
    term_set: TermSet

    # Semantic version.
    version: str

    # Version publication date.
    version_date: datetime.datetime

    def __str__(self) -> str:
        """Instance string representation."""
        return f"{self.version}|{self.version_date}"

    @property
    def enum_set(self) -> typing.Generator:
        """Set of enumerations defined within dictionary."""
        targets = \
            [i for i in self.term_set if i.is_enum] + \
            [
                self.contract_event_type,
                self.contract_reference_role,
                self.contract_reference_type,
            ]

        for target in sorted(targets, key=lambda i: i.identifier):
            yield target
