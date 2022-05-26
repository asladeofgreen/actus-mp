import datetime
import typing

import json
import os
import pathlib


# Path to actus-dictionary.json file.
_FILE: pathlib.Path = pathlib.Path(os.path.dirname(__file__)) / "actus-dictionary.json"


class Accessor():
    """Encapsulates access to actus-dictionary.json.
    
    """
    def __init__(self):
        with open(_FILE, "r") as fstream:
            self._actus_dictionary = json.loads(fstream.read())
    
    @property
    def applicability(self) -> typing.List[dict]:
        return self._actus_dictionary["applicability"].values()

    @property
    def contract_type_set(self) -> typing.List[dict]:
        return self._actus_dictionary["taxonomy"].values()

    @property
    def state_set(self) -> typing.List[dict]:
        return self._actus_dictionary["states"].values()

    @property
    def term_set(self) -> typing.List[dict]:
        return self._actus_dictionary["terms"].values()

    @property
    def version(self) -> str:
        return self._actus_dictionary["version"]["Version"]

    @property
    def version_date(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self._actus_dictionary["version"]["Date"])
