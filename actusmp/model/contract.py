import dataclasses
import typing

from actusmp.model.enum_ import Enum
from actusmp.model.term import TermSet


@dataclasses.dataclass
class Contract():
    """A node within the ACTUS taxonomy representing a financial contract associated with 
       an algorithm for deriving cash flow exposure amoungst a set of counter-parties.
    
    """
    # Upper case 3/4 character type identifier, e.g. 'ANN'.
    acronym: str

    # Contextual economic classification, e.g. 'Fixed Income'.
    classification: str
    
    # Contextual economic coverage, e.g. 'classical level payment mortgages'.
    coverage: str

    # Fuller description of contract type's macro function.    
    description: str
    
    # Contextual economic instrument family, e.g. 'Basic'.
    family: str
    
    # Unique contract type identifier, e.g. 'annuity'.
    identifier: str

    # Contract type name, e.g. 'Annuity'.
    name: str
    
    # Publication status, e.g. 'Released'.
    status: str
    
    # Set of associated terms.
    term_set: TermSet = None

    def __hash__(self):
        """Instance hash representation."""
        return hash(self.identifier)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"contract|{self.acronym}..{self.identifier}|{len(self.term_set)}"

    @property
    def contract_type(self) -> Enum:
        """Gets type of contract under consideration."""
        return self.term_set.get_term("contractType")


@dataclasses.dataclass
class ContractSet():
    """A set of financial contracts within the ACTUS taxomony.
    
    """
    # Collection of associated contracts.
    _items: typing.List[Contract] 

    def __iter__(self) -> typing.Iterator[Contract]:
        """Instance iterator."""
        return iter(sorted(self._items, key=lambda i: i.acronym))    

    def __len__(self) -> int:
        """Instance iterator length."""
        return len(self._items)

    def __str__(self) -> str:
        """Instance string representation."""
        return f"contract-set|{len(self)}"

    def get_contract(self, identifier: str):
        """Returns first contract within associated collection with matching identifier."""
        for item in self:
            if item.identifier == identifier:
                return item
