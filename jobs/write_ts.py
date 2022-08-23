import pathlib
import actusmp

_LANG = actusmp.TargetLanguage.typescript
_PATH_ROOT = pathlib.Path("/home/sphere0/Work/nf/actus")

actusmp.write_typeset(
    _LANG,
    _PATH_ROOT / "actus-core-js" / "src"
    )

actusmp.write_funcset(
    _LANG,
    _PATH_ROOT / "actus-core-js" / "src",
    _PATH_ROOT / "actus-core"
    )
