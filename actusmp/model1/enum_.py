import dataclasses
import typing


@dataclasses.dataclass
class EnumMember():
    """Member of an enumerated type.
    
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

    def __str__(self) -> str:
        """Instance string representation."""
        return f"enum-member|{self.identifier}.{self.acronym}.{self.option}"

    def is_match(self, identifier: str):
        """Predicate that returns true if identifier can be matched."""
        return identifier.upper() in [self.acronym.upper(), self.identifier.upper()]


@dataclasses.dataclass
class Enum():
    """An enumerated type that encloses a constrained set of members.
    
    """
    # Upper case 3/4 character type identifier, e.g. 'IPAC'.
    acronym: str

    # Fuller description of term's raison d'etre.    
    description: str

    # Term name, e.g. 'Accrued Interest'.
    name: str

    # Formal term identifier, e.g. 'accruedInterest'.
    identifier: str

    # Collection of associated enumeration members.
    members: typing.List[EnumMember] 

    def __iter__(self) -> typing.Iterator[EnumMember]:
        """Instance iterator."""
        return iter(sorted(self.members, key=lambda i: i.option))    

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self.members)

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
            return self.get_member("OOO")


    def get_member(self, member_id: str) -> EnumMember:
        """Returns first member matched by identifier."""
        for item in self:
            if item.is_match(member_id):
                return item
