import sys,os,unittest
from unittest import main, TestCase
mypath=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(mypath)

from src.business.access_data_base import conectar, fecha_conexao
from src.exception.duplicated_cpf_error import DuplicatedCPF
from src.exception.field_error import EmptyFieldError, InvalidFieldError
from src.exception.funcionario_not_found import FuncionarioNotFoundError
from src.exception.base_funcionario_error import EmptyDataBaseError
from src.business.cadastro_funcionario import CadastroFuncionario
from src.entities.funcionario import Funcionario

class TestCadastroFuncionario(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        '''Esvazia o Banco de dados e inicia o cadastro'''
        cnx = conectar()

        cursor = cnx.cursor()
        query = (
            '''SELECT  CPF FROM xpto_alimentos.funcionario ''')

        cursor.execute(query)

        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        for cpf in cpf_list:
            cls.cadastro.excluir(cpf)
        fecha_conexao(cnx, cursor)

        cls.cadastro = CadastroFuncionario()

        print('run SetUpclass')

    @classmethod
    def tearDown(cls) -> None:
        '''Esvazia o Banco de dados'''
        cnx = conectar()

        cursor = cnx.cursor()
        query = (
            '''SELECT  CPF FROM xpto_alimentos.funcionario ''')

        cursor.execute(query)

        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        for cpf in cpf_list:
            cls.cadastro.excluir(cpf)
        fecha_conexao(cnx, cursor)

    def test_cadastro_consultar(self):
        funcionario1 = Funcionario(
            "Ana Maria Silva", "11111111100", "2019-02-07", "32", "Sim")
        funcionario2 = Funcionario(
            'Bernardo Santos', '22222222200', '2017-10-16', '20', 'Nao')

        self.cadastro.inserir(funcionario1)
        self.cadastro.inserir(funcionario2)

        resultado = self.cadastro.consultar("11111111100")

        self.assertEqual("11111111100", resultado.CPF)

    def test_cadastro_inserir(self):
        funcionario = Funcionario(
            "Ana Maria Silva", "11111111100", "2019-02-07", "32", "Sim")
        self.cadastro.inserir(funcionario)
        resultado = self.cadastro.consultar(funcionario.CPF)

        self.assertEqual("11111111100", resultado.CPF)

    def test_cadastro_listar_funcionarios(self):
        funcionario1 = Funcionario(
            "Ana Maria Silva", "11111111100", "2019-02-07", "32", "Sim")
        funcionario2 = Funcionario(
            'Bernardo Santos', '22222222200', '2017-10-16', '20', 'Nao')

        self.cadastro.inserir(funcionario1)
        self.cadastro.inserir(funcionario2)
        resultado=self.cadastro.listar_funcionarios()
        
        self.assertEqual(('Ana Maria Silva','Bernardo Santos'),(resultado[0].nome,resultado[1].nome))

    def test_cadastro_consultar_error(self):
        with self.assertRaises(FuncionarioNotFoundError):
            self.cadastro.consultar("11111111100")

    def test_cadastro_excluir(self):
        funcionario = Funcionario(
            "Ana Maria Silva", "11111111100", "2019-02-07", "32", "Sim")
        self.cadastro.inserir(funcionario)
        self.cadastro.excluir(funcionario.CPF)

        with self.assertRaises(FuncionarioNotFoundError):
            self.cadastro.consultar("11111111100")

    def test_cadastro_listar_funcionarios_error(self):
        with self.assertRaises(EmptyDataBaseError):
            self.cadastro.listar_funcionarios()

    def test_cadastro_excluir_error(self):
        with self.assertRaises(FuncionarioNotFoundError):
            self.cadastro.excluir("11111111100")

    def test_cadastro_inserir_id_error(self):
        funcionario = Funcionario(
            "Ana Maria Silva", "11111111100", "2019-02-07", "33", "Sim")
        with self.assertRaises(InvalidFieldError):
            self.cadastro.inserir(funcionario)

    def test_cadastro_inserir_duplicatedcpf_error(self):
        funcionario1 = Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "32", "Sim")
        funcionario2 = Funcionario('Daiana Santana de Sousa', "11111111100", '2002-04-09', "30", 'Sim')
        self.cadastro.inserir(funcionario2)

        with self.assertRaises(DuplicatedCPF):
            self.cadastro.inserir(funcionario2)

    def test_cadastro_inserir_emptyfield_error(self):
        funcionario1 = Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "", "Sim")
        with self.assertRaises(EmptyFieldError):
            self.cadastro.inserir(funcionario1)

    def test_cadastro_inserir_invalidfield_error(self):
        funcionario1 = Funcionario("Ana Maria Silva", "1111111100", "2019-02-07", "", "Sim")
        with self.assertRaises(InvalidFieldError):
            self.cadastro.inserir(funcionario1)

if __name__ == '__main__':
    unittest.main()
