import dataclasses
import typing

from actusmp.model.entity import Entity


@dataclasses.dataclass
class EnumMember(Entity):
    """Member of an enumerated type.

    """
    # Flag indicating whether member is enumeration scope default.
    is_default: typing.Optional[bool]

    # Ordinal position within enumeration scope.
    option: int


@dataclasses.dataclass
class Enum(Entity):
    """An enumerated type that encloses a constrained set of members.

    """
    # Collection of associated enumeration members.
    members: typing.List[EnumMember]

    def __hash__(self) -> int:
        """Instance hash representation."""
        return hash(f"enum|{self.acronym}|{self.identifier}")

    def __iter__(self) -> typing.Iterator[EnumMember]:
        """Instance iterator."""
        return iter(sorted(self.members, key=lambda i: i.option))

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self.members)
