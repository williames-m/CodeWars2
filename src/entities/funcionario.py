import os,sys
mypath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(mypath)
from src.entities.cargo import Cargo
from src.business.access_data_base import conectar, fecha_conexao


class Funcionario():
    def __init__(self, nome: str, CPF: str, data_admissao: str, cargo_id: str, comissao: str,matricula='0') -> None:
        self.__matricula = matricula
        self.__nome: str = nome
        self.__CPF: str = CPF
        self.__data_admissao: str = data_admissao
        self.__comissao: str = comissao
        self.__cargo_id: str = cargo_id

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def CPF(self) -> str:
        return self.__CPF

    @property
    def data_admissao(self) -> str:
        return self.__data_admissao

    @property
    def comissao(self) -> str:
        return self.__comissao

    @property
    def cargo_id(self) -> str:
        return self.__cargo_id
        
    @property
    def matricula(self) -> str:
        return self.__matricula

    def cargo(self) -> Cargo:
        '''
        Retorna a classe cargo associada ao id de dargo do funcionario
        '''
        cnx = conectar()

        cursor = cnx.cursor()

        query = (
            '''SELECT id,descricao,salario_base, comissao 
        FROM cargo 
        WHERE id=%s'''
        )

        cursor.execute(query, [self.cargo_id])
        for (codigo, descricao, salario_base, comissao) in cursor:
            cargo = Cargo(codigo, descricao, salario_base, comissao)

        fecha_conexao(cnx,cursor)
        return cargo
