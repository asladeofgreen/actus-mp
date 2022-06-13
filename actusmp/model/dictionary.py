import dataclasses
import datetime
import typing

from actusmp.model.applicability import Applicability
from actusmp.model.contract import ContractSet
from actusmp.model.enum_ import Enum
from actusmp.model.term import TermSet
from actusmp.model.states import StateSet


@dataclasses.dataclass
class Dictionary():
    """An information set by which the ACTUS standard is declared.
    
    """
    # Criteria that determine which set of terms are associated with which type of contract. 
    applicability: Applicability

    # Set of associated contract reference enums.
    contract_reference_enum_set: typing.List[Enum]

    # Set of associated contract types.
    contract_set: ContractSet

    # Global set of associated contract terms.
    global_term_set: TermSet

    # Set of states through which a contract may pass during it's lifetime.
    state_set: StateSet

    # Semantic version.
    version: str

    # Version publication date.
    version_date: datetime.datetime

    def __str__(self) -> str:
        """Instance string representation."""
        return f"{self.version}|{self.version_date}"

    @property
    def global_enum_set(self):
        """Global set of associated contract terms that are enumerations."""
        return self.global_term_set.enum_set

    @property
    def applicable_contracts(self):
        """Set of contracts that are deemed applicable, i.e. have 
           non-empty associated term sets."""
        for contract in [i for i in self.contract_set if i.term_set]:
            yield contract
