import datetime
import json
import os
import pathlib
import typing

from actusmp.dictionary.parser import parse


# Path to actus-dictionary.json file.
_FILE: pathlib.Path = pathlib.Path(os.path.dirname(__file__)) / "actus-dictionary.json"


class Accessor():
    """Encapsulates access to actus-dictionary.json.
    
    """
    def __init__(self):
        with open(_FILE, "r") as fstream:
            self._actus_dictionary = parse(json.loads(fstream.read()))
    
    @property
    def applicability(self) -> typing.List[dict]:
        return self._actus_dictionary["applicability"].items()

    @property
    def contract_event_type(self) -> dict:
        return self._actus_dictionary["event"]["eventType"]

    @property
    def contract_type_set(self) -> typing.List[dict]:
        return self._actus_dictionary["taxonomy"].values()

    @property
    def contract_reference_role(self) -> dict:
        return self._actus_dictionary["contractReference"]["role"]

    @property
    def contract_reference_type(self) -> dict:
        return self._actus_dictionary["contractReference"]["type"]

    @property
    def state_set(self) -> typing.List[dict]:
        return self._actus_dictionary["states"].values()

    @property
    def taxonomy(self) -> typing.List[dict]:
        return self._actus_dictionary["taxonomy"].values()

    @property
    def term_set(self) -> typing.List[dict]:
        return self._actus_dictionary["terms"].values()

    @property
    def version(self) -> str:
        return self._actus_dictionary["version"]["Version"]

    @property
    def version_date(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self._actus_dictionary["version"]["Date"])
