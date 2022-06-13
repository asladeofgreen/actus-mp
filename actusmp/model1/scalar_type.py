import enum


class ScalarType(enum.Enum):
    """Set of scalar field types.

    """
    ContractReference = enum.auto()
    Cycle = enum.auto()
    Enum = enum.auto()
    Period = enum.auto()
    Real = enum.auto()
    Timestamp = enum.auto()
    Unknown = enum.auto()
    Varchar = enum.auto()
