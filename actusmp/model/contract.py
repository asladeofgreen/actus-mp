import dataclasses
import typing

from actusmp.model.enum_ import Enum
from actusmp.model.scalar_type import ScalarType
from actusmp.model.term import Term
from actusmp.model.term import TermSet
from actusmp.model.taxonomy import ContractTypeInfo


@dataclasses.dataclass
class Contract():
    """A node within the ACTUS taxonomy representing a financial contract associated with 
       an algorithm for deriving cash flow exposure amoungst a set of counter-parties.
    
    """
    # Set of applicable terms.
    term_set: TermSet

    # Associated type information such as acronym, identifier ...etc.
    type_info: ContractTypeInfo
    
    def __hash__(self):
        """Instance hash representation."""
        return hash(self.identifier)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"contract|{self.type_info.acronym}|{len(self.term_set)}"


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

    def get_contract(self, contract_id: str):
        """Returns first contract within associated collection with matching identifier.
        
        """
        for item in self:
            if item.identifier == contract_id:
                return item
