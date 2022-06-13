import dataclasses
import datetime
import typing

from actusmp.model1.contract_reference import ContractReferenceInfo
from actusmp.model1.enum_ import Enum
from actusmp.model1.states import StateSet
from actusmp.model1.taxonomy import Taxonomy
from actusmp.model1.terms import TermSet


@dataclasses.dataclass
class Dictionary():
    """An information set by which the ACTUS standard is declared.
    
    """
    # Enumeration over set Intra-contract reference information.
    contract_reference_role: Enum

    # Intra-contract reference information.
    contract_reference_type: Enum

    # Enumeration over set of contract event types.
    contract_event_type: Enum

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
