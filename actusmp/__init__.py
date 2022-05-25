#  ░█████╗░░█████╗░████████╗██╗░░░██╗░██████╗░░░░░░███╗░░░███╗██████╗░
#  ██╔══██╗██╔══██╗╚══██╔══╝██║░░░██║██╔════╝░░░░░░████╗░████║██╔══██╗
#  ███████║██║░░╚═╝░░░██║░░░██║░░░██║╚█████╗░█████╗██╔████╔██║██████╔╝
#  ██╔══██║██║░░██╗░░░██║░░░██║░░░██║░╚═══██╗╚════╝██║╚██╔╝██║██╔═══╝░
#  ██║░░██║╚█████╔╝░░░██║░░░╚██████╔╝██████╔╝░░░░░░██║░╚═╝░██║██║░░░░░
#  ╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░░╚═════╝░╚═════╝░░░░░░░╚═╝░░░░░╚═╝╚═╝░░░░░

__title__ = "actusmp"
__version__ = "0.0.1"
__author__ = "Mark A. Greenslade et al"
__license__ = "Apache 2.0"


from actusmp.codegen import TargetLanguage
from actusmp.codegen import write_typeset
from actusmp.codegen import write_funcset

from actusmp.model import Contract
from actusmp.model import ContractSet
from actusmp.model import Term
from actusmp.model import TermSet
from actusmp.model import Dictionary
