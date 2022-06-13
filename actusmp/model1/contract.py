import dataclasses
import typing

from actusmp.model1.enum_ import Enum
from actusmp.model1.scalar_type import ScalarType
from actusmp.model1.terms import Term
from actusmp.model1.terms import TermSet
from actusmp.model1.taxonomy import ContractTypeInfo


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
        return f"contract|{self.type_info}..{self.identifier}|{len(self.term_set)}"


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

    def get_contract(self, contract_id: str):
        """Returns first contract within associated collection with matching identifier.
        
        """
        for item in self:
            if item.identifier == contract_id:
                return item


@dataclasses.dataclass
class ContractTerm():
    """A contractual term associated with a specific type of financial contract.
    
    """
    # Upper case 3/4 character type identifier, e.g. 'IPAC'.
    acronym: str

    # Constraint over set of allowed values, e.g. 'ISO8601 Datetime'.
    allowed_values: typing.List[typing.Union[dict, str]]

    # Default value.
    default: typing.Optional[str]

    # Fuller description of term's raison d'etre.    
    description: str

    # Identifier of associated group, e.g. 'Interest'
    group_id: str

    # Formal term identifier, e.g. 'accruedInterest'.
    identifier: str
    
    # Flag indicating whether the term declares an array or not.
    is_array: bool

    # Term name, e.g. 'Accrued Interest'.
    name: str

    # Associated scalar data type, e.g. Timestamp | Real | Enum ... etc.
    scalar_type: ScalarType

    def __str__(self) -> str:
        """Instance string representation."""
        return f"term|{self.identifier}"