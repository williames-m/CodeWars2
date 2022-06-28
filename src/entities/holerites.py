import os,sys
mypath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(mypath)
print(mypath)
from src.business.bases_salariais import INSS, IRRF
from src.business.cadastro_funcionario import CadastroFuncionario
from src.entities.funcionario import Funcionario

class Holerite():
    def __init__(self, cpf: str, mes: int, faltas: int=0):
        self.__mes_referencia = mes
        self.__cpf = cpf
        self.__faltas = faltas

        # -----------Gerado consultando base de dados e por calculo----------
        self.__comissao: float = self.funcionario().cargo().comissao
        self.__salario_base: float = self.funcionario().cargo().salario_base

    def funcionario(self) -> Funcionario:
        cadastro = CadastroFuncionario()
        funcionario = cadastro.consultar(self.cpf)
        return funcionario

    @property
    def mes_referencia(self) -> int:
        return self.__mes_referencia

    @property
    def salario_base(self) -> float:
        return self.__salario_base

    @property
    def comissao(self) -> float:
        return self.__comissao

    @property
    def faltas(self) -> int:
        return self.__faltas

    @property
    def cpf(self) -> float:
        return self.__cpf
    