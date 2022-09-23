import dataclasses
import typing

from actusmp.model.scalar_type import ScalarType
from actusmp.model.taxonomy import ContractTypeInfo
from actusmp.model.term import TermSet


@dataclasses.dataclass
class Contract():
    """A node within the ACTUS taxonomy representing a financial contract associated with
       an algorithm for deriving cash flow exposure amoungst a set of counter-parties.

    """
    # Set of applicable terms.
    term_set: TermSet

    # Associated type information such as acronym, identifier ...etc.
    type_info: ContractTypeInfo

    def __hash__(self) -> int:
        """Instance hash representation."""
        return hash(f"contract|{self.acronym}|{self.identifier}")

    def __str__(self) -> str:
        """Instance string representation."""
        return f"contract|{self.acronym}|{self.identifier}|{len(self.term_set)}"

    @property
    def acronym(self):
        """Returns unique long label identifier."""
        return self.type_info.acronym

    @property
    def identifier(self):
        """Returns unique short label identifier."""
        return self.type_info.identifier

    def uses_scalar_type(self, scalar_type: ScalarType) -> bool:
        """Returns flag indicating whether an associated term has a matching scalar type.

        :scalar_type: A scalar type potentially associated with a term.
        :returns: True if matched else False.

        """
        for term in self.term_set:
            if term.scalar_type == scalar_type:
                return True
        return False


@dataclasses.dataclass
class ContractSet():
    """A set of financial contracts within the ACTUS taxomony.

    """
    # Collection of associated contracts.
    _items: typing.List[Contract]

    def __iter__(self) -> typing.Iterator[Contract]:
        """Instance iterator."""
        return iter(sorted(self._items, key=lambda i: i.type_info.acronym))

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self._items)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"contract-set|{len(self)}"

    def get_contract(self, contract_id: str) -> typing.Optional[Contract]:
        """Returns first contract within associated collection with matching identifier.

        :param contract_id: Identifier of a contract.
        :returns: A contract matched by it's id.

        """
        for item in self:
            if item.identifier == contract_id:
                return item
