import dataclasses
import enum
import typing

from actusmp.model.entity import Entity


class ContractTypePublicationStatus(enum.Enum):
    """Current publication status of contract type.

    """
    Implemented = enum.auto()
    Planned = enum.auto()
    Released = enum.auto()
    Unknown = enum.auto()


@dataclasses.dataclass
class ContractTypeInfo(Entity):
    """A node within the ACTUS taxonomy representing a financial contract associated with
       an algorithm for deriving cash flow exposure amoungst a set of counter-parties.

    """
    # Contextual economic classification, e.g. 'Fixed Income'.
    classification: str

    # Contextual economic coverage, e.g. 'classical level payment mortgages'.
    coverage: str

    # Contextual economic instrument family, e.g. 'Basic'.
    family: str

    # Publication status, e.g. 'Released'.
    publication_status: ContractTypePublicationStatus

    def __hash__(self):
        """Instance hash representation."""
        return hash(self.identifier)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"contract-type|{self.acronym}..{self.identifier}"


@dataclasses.dataclass
class Taxonomy():
    """Contains sets of appplicable terms related to contracts.

    """
    # Collection of associated applicable contract terms.
    _items: typing.List[ContractTypeInfo]

    def __iter__(self) -> typing.Iterator[ContractTypeInfo]:
        """Instance iterator."""
        return iter(sorted(self._items, key=lambda i: i.acronym))

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self._items)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"Taxonoty|{len(self)}"
