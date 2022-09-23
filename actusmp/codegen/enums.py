import enum

from actusmp.model import FunctionType


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


# Map: TargetLanguage <-> template subfolder name.
LANG_TEMPLATE_SUBFOLDER: dict = {
    TargetLanguage.python: "py",
    TargetLanguage.rust: "rs",
    TargetLanguage.typescript: "ts",
}


# Map: Generator type <-> ACTUS function type.
GENERATOR_ACTUS_FN = {
    TargetGenerator.FuncStubPOF: FunctionType.POF,
    TargetGenerator.FuncStubSTF: FunctionType.STF,
}
