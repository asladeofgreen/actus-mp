import enum


class TargetLanguage(enum.Enum):
    """Enumeration: set of supported language targets.
    
    """
    typescript = enum.auto()
    python = enum.auto()
    rust = enum.auto()


class TargetGenerator(enum.Enum):
    """Enumeration: set of supported generator types.
    
    """
    Enum = enum.auto()
    EnumIndex = enum.auto()
    FuncIndex = enum.auto()
    FuncStubPOF = enum.auto()
    FuncStubSTF = enum.auto()
    FuncStubIndex = enum.auto()
    FuncStubMain = enum.auto()
    StateSpace = enum.auto()
    Termset = enum.auto()
    TermsetIndex = enum.auto()
