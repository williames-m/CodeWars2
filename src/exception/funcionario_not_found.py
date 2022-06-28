import sys,os,unittest
from unittest import main, TestCase
mypath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(mypath)
from src.exception.not_found_error import NotFoundError

class FuncionarioNotFoundError(NotFoundError):
    
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
