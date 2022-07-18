import dataclasses
import typing


@dataclasses.dataclass
class Entity():
    """A uniquely identifable entity within the type system.
    
    """
    # A short identifier, e.g. 'SCF'.
    acronym: str

    # A long text description, e.g. 'Shift event dates first then ...'. 
    description: str

    # A canonical identifier within enumeration scope.
    identifier: str

    # Flag indicating whether member is enumeration scope default.
    is_default: typing.Optional[bool]

    # A formal name within enumeration scope.
    name: str

    # Ordinal position within enumeration scope.
    option: int

    def __hash__(self):
        """Instance hash representation."""
        return hash(str(self))

    def __str__(self) -> str:
        """Instance string representation."""
        return f"enum-member|{self.identifier}.{self.acronym}.{self.option}"

    def is_match(self, identifier: str):
        """Predicate that returns true if identifier can be matched."""
        return identifier.upper() in [self.acronym.upper(), self.identifier.upper()]
