import dataclasses

from actusmp.model1.enum_ import Enum


@dataclasses.dataclass
class ContractReferenceInfo():
    """Information associated with specifying references between contracts.
    
    """
    # Upper case 3/4 character type identifier, e.g. 'ANN'.
    role: Enum

    # Contextual economic classification, e.g. 'Fixed Income'.
    typeof: Enum
