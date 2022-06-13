import dataclasses
import typing

from actusmp.model1.scalar_type import ScalarType


@dataclasses.dataclass
class State():
    """A state field assigned during calculation execution.
    
    """
    # A short identifier, e.g. 'SD'.
    acronym: str

    # Constraint over set of allowed values, e.g. 'ISO8601 Datetime'.
    allowed_values: typing.List[typing.Union[dict, str]]

    # Description of state field, e.g. 'The multiplier being applied to principal cash flows'.
    description: str

    # Formal state field identifier, e.g. 'statusDate'.
    identifier: str

    # Formal state field name, e.g. 'Status Date'.
    name: str

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
