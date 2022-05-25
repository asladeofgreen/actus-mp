import dataclasses
import typing

from actusmp.model.term import Term


@dataclasses.dataclass
class EnumMember():
    # A short identifier, e.g. 'SCF'.
    acronym: str

    # A long text description, e.g. 'Shift event dates first then ...'. 
    description: str

    # A canonical identifier within enumeration scope.
    identifier: str

    # A formal name within enumeration scope.
    name: str

    # Ordinal position within enumeration scope.
    option: int

    def __str__(self) -> str:
        """Instance string representation."""
        return f"enum-member|{self.option}.{self.acronym}.{self.identifier}"

    def is_match(self, identifier: str):
        """Predicate that returns true if identifier can be matched."""
        return identifier.upper() in [self.acronym.upper(), self.identifier.upper()]


@dataclasses.dataclass
class Enum(Term):
    # Collection of associated enumeration members.
    _members: typing.List[EnumMember] 

    def __iter__(self) -> typing.Iterator[EnumMember]:
        """Instance iterator."""
        return iter(sorted(self._members, key=lambda i: i.option))    

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self._members)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"enum|{self.acronym}.{self.name}.{len(self)}"

    @property
    def default_member(self):
        """Returns associated default member."""
        if self.default is None:
            return

        # Match by identifier.                
        for item in self:
            if item.is_match(self.default):
                return item

        # Exceptions - to be reviewed.
        if self.identifier == "penaltyType":
            return self.get_member("N")
        if self.identifier == "scalingEffect":
            return self.get_member("000")

    def get_member(self, member_id: str) -> EnumMember:
        """Returns first member matched by identifier."""
        for item in self:
            if item.is_match(member_id):
                return item
