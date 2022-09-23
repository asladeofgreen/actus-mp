import dataclasses
import typing

from actusmp.model.entity import Entity
from actusmp.model.scalar_type import ScalarType


@dataclasses.dataclass
class Term(Entity):
    """A contractual term associated with a specific type of financial contract.

    """
    # Constraint over set of allowed values, e.g. 'ISO8601 Datetime'.
    allowed_values: typing.List[typing.Union[dict, str]]

    # Default value.
    default: typing.Optional[str]

    # Identifier of associated group, e.g. 'Interest'
    group_id: str

    # Flag indicating whether term declaration defines an array.
    is_array: bool

    # Associated scalar data type, e.g. Timestamp | Real | Enum ... etc.
    scalar_type: ScalarType

    @property
    def has_default(self) -> bool:
        """Returns flag indicating whether the term field has a default value."""
        if self.scalar_type in (ScalarType.Cycle, ScalarType.Period):
            return False
        return self.default is not None

    @property
    def is_enum(self) -> bool:
        """Returns flag indicating whether the term field type is an enumeration."""
        return self.scalar_type == ScalarType.Enum

    @property
    def members(self):
        """Helper attribute when processing enum terms."""
        return self.allowed_values if self.is_enum else []


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
