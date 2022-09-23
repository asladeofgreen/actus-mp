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
            self._obj: dict = parse(json.loads(fstream.read()))

    @property
    def applicability(self) -> typing.List[dict]:
        return self._obj["applicability"].items()

    @property
    def contract_event_type(self) -> dict:
        return self._obj["event"]["eventType"]

    @property
    def contract_reference_role(self) -> dict:
        return self._obj["contractReference"]["role"]

    @property
    def contract_reference_type(self) -> dict:
        return self._obj["contractReference"]["type"]

    @property
    def contract_performance(self) -> dict:
        return self._obj["terms"]["contractPerformance"]

    @property
    def contract_role(self) -> dict:
        return self._obj["terms"]["contractRole"]

    @property
    def contract_type(self) -> dict:
        return self._obj["terms"]["contractType"]

    @property
    def state_set(self) -> typing.List[dict]:
        return self._obj["states"].values()

    @property
    def taxonomy(self) -> typing.List[dict]:
        return self._obj["taxonomy"].values()

    @property
    def term_set(self) -> typing.List[dict]:
        return self._obj["terms"].values()

    @property
    def version(self) -> str:
        return self._obj["version"]["Version"]

    @property
    def version_date(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self._obj["version"]["Date"])
