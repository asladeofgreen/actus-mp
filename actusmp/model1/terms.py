import dataclasses
import typing

from actusmp.model1.scalar_type import ScalarType


@dataclasses.dataclass
class Term():
    """A contractual term associated with a specific type of financial contract.
    
    """
    # Upper case 3/4 character type identifier, e.g. 'IPAC'.
    acronym: str

    # Constraint over set of allowed values, e.g. 'ISO8601 Datetime'.
    allowed_values: typing.List[typing.Union[dict, str]]

    # Default value.
    default: typing.Optional[str]

    # Fuller description of term's raison d'etre.    
    description: str

    # Identifier of associated group, e.g. 'Interest'
    group_id: str

    # Formal term identifier, e.g. 'accruedInterest'.
    identifier: str

    # Flag indicating whether the term declares an array or not.
    is_array: bool

    # Term name, e.g. 'Accrued Interest'.
    name: str

    # Associated scalar data type, e.g. Timestamp | Real | Enum ... etc.
    scalar_type: ScalarType

    def __str__(self) -> str:
        """Instance string representation."""
        return f"term|{self.identifier}"


@dataclasses.dataclass
class TermSet():
    """A set of contractual terms associated with a specific type of financial contract.
    
    """
    # Collection of associated contract terms.
    _terms: typing.List[Term]

    def __iter__(self) -> typing.Iterator[Term]:
        """Instance iterator."""
        return iter(sorted(self._terms, key=lambda i: i.identifier))    

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self._terms)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"term-set|{len(self)}"

    def get_term(self, identifier: str) -> Term:
        """Returns first term matched by identifier."""
        for item in self:
            if item.identifier == identifier:
                return item

    def get_by_group_id(self, group_id: str) -> "TermSet":
        """Returns set of terms matched by group identifier."""
        return TermSet([i for i in self if i.group_id == group_id])

    @property
    def enum_set(self):
        """Returns sub-set of terms that are enumerations."""
        return TermSet([i for i in self if i.scalar_type == ScalarType.Enum])
