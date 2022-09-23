import enum


class FunctionType(enum.Enum):
    """Enumeration over set of contract state function types.

    """
    # Payoff function.
    POF = enum.auto()

    # State transition function.
    STF = enum.auto()
