import dataclasses
import typing

from actusmp.model.taxonomy import ContractTypeInfo


@dataclasses.dataclass
class ApplicableTermInfo():
    """Information related to an term applicable to a contract.

    """
    # Identifier of associated contract type.
    contract_type_id: str

    # Identifier of associated term.
    term_id: str

    # Upstream processing information associated with term.
    term_instruction: str

    def __str__(self) -> str:
        """Instance string representation."""
        return f"applicable-term-info|{self.contract_type_id}|{self.term_id}"

    @property
    def sort_key(self) -> str:
        """A key used in sorting scenarios."""
        return f"{self.contract_type_id}|{self.term_id}"


@dataclasses.dataclass
class ApplicableTermInfoSet():
    """Global set of terms applicable to contracts.

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
        return f"applicable-term-info-set|{len(self)}"

    def get_applicable_termset(self, type_info: ContractTypeInfo) -> typing.Generator:
        """Returns set of applicable term information filtered by contract type.

        :param type_info: Type information associated with a contract.
        :returns: Sequence of applicable terms.

        """
        for info in self:
            if info.contract_type_id == type_info.identifier:
                yield info
