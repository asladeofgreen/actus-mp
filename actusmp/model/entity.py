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

    # A formal name within enumeration scope.
    name: str

    def __hash__(self):
        """Instance hash representation."""
        return hash(str(self))

    def __str__(self) -> str:
        """Instance string representation."""
        return f"{self.__class__.__name__} :: {self.identifier} | {self.acronym}"

    def is_match(self, identifier: str):
        """Predicate: returns true if identifier can be matched."""
        return identifier.upper() in [self.acronym.upper(), self.identifier.upper()]


@dataclasses.dataclass
class IterableEntity():
    """An entity managing an inner collection.

    """
    # Collection of associated contract terms.
    _terms: typing.List[Entity]

    def __iter__(self) -> typing.Iterator[Entity]:
        """Instance iterator."""
        return iter(sorted(self._terms, key=lambda i: i.identifier))

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self._terms)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"term-set|{len(self)}"

    def get_item(self, identifier: str) -> Entity:
        """Returns first item matched by identifier."""
        for item in self:
            if item.identifier == identifier:
                return item
