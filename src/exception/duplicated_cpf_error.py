import os,sys
mypath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(mypath)
from src.exception.base_funcionario_error import DataBaseError

class DuplicatedCPF(DataBaseError):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
