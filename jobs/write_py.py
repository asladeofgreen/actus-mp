import pathlib
import actusmp

_LANG = actusmp.TargetLanguage.python
_PATH_ROOT = pathlib.Path("/home/sphere0/Work/nf/actus")

actusmp.write_typeset(
    _LANG,
    _PATH_ROOT / "actus-core-py" / "pyactus"
    )

actusmp.write_funcset(
    _LANG,
    _PATH_ROOT / "actus-core-py" / "pyactus",
    _PATH_ROOT / "actus-core"
    )
