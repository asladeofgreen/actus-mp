import dataclasses
import typing

from actusmp.model.entity import Entity
from actusmp.model.scalar_type import ScalarType


@dataclasses.dataclass
class State(Entity):
    """A state field assigned during calculation execution.

    """
    # Constraint over set of allowed values, e.g. 'ISO8601 Datetime'.
    allowed_values: typing.List[typing.Union[dict, str]]

    # Flag indicating whether the state field declares an array or not.
    is_array: bool

    # Associated scalar data type, e.g. Timestamp | Real | Enum ... etc.
    scalar_type: ScalarType

    def __str__(self) -> str:
        """Instance string representation."""
        return f"state|{self.identifier}"

    @property
    def short_description(self) -> str:
        """Returns a short description."""
        return self.description.replace("\n", "")


@dataclasses.dataclass
class StateSet():
    """A collection of contract state fields that are assigned
       during calculation execution.

    """
    # Collection of associated contract states.
    _states: typing.List[State]

    def __iter__(self) -> typing.Iterator[State]:
        """Instance iterator."""
        return iter(sorted(self._states, key=lambda i: i.identifier))

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self._states)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"state-set|{len(self)}"
