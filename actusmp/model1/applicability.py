import dataclasses
import typing


@dataclasses.dataclass
class ApplicableTermInfo():
    """Information related to a applicability contraints related to a contractual term.
    
    """
    # Identifier of associated contract type.
    contract_id: str

    # Identifier of associated term.
    term_id: str

    # Upstream processing information associated with term.
    term_instruction: str

    def __str__(self) -> str:
        """Instance string representation."""
        return f"applicability-item|{self.contract_id}|{self.term_id}|{self.term_instruction}"

    @property
    def sort_key(self):
        """A key used in sorting scenarios."""
        return f"{self.contract_id}|{self.term_id}"


@dataclasses.dataclass
class Applicability():
    """Contains sets of appplicable terms related to contracts.

    """
    # Collection of associated applicable contract terms.
    _items: typing.List[ApplicableTermInfo] 

    def __iter__(self) -> typing.Iterator[ApplicableTermInfo]:
        """Instance iterator."""
        return iter(sorted(self._items, key=lambda i: i.sort_key))    

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self._items)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"applicability|{len(self)}"

    def get_applicable_terms(self, contract_id: str) -> typing.List[ApplicableTermInfo]:
        """Returns set of items matched by contract type identifier.
        
        """
        return [i for i in self if i.contract_id == contract_id]
