from mysql.connector import connect
import sys,os,pandas
from tabulate import tabulate
mypath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(mypath)

from src.exception.base_funcionario_error import EmptyDataBaseError
from src.exception.field_error import EmptyFieldError, InvalidFieldError
from src.exception.duplicated_cpf_error import DuplicatedCPF
from src.business.access_data_base import conectar, fecha_conexao
from src.entities.funcionario import Funcionario
sys.path.append(r"C:\Users\ligia\Documents\autoensino\Coding\CodeWarsII")

from src.exception.funcionario_not_found import FuncionarioNotFoundError
from mysql.connector.errors import IntegrityError,DatabaseError

class CadastroFuncionario():

    def __init__(self):
        self.__campos: list = ['nome', 'CPF',
                               'data_admissao', 'cargo_id', 'comissao']

    def inserir(self, funcionario: Funcionario):
        cnx = conectar()

        cursor = cnx.cursor()

        adiciona_funcionario = (
            """INSERT INTO funcionario
            (nome,CPF,data_admissao,cargo_id,comissao ) 
            VALUES ( %(nome)s, %(CPF)s, %(data_admissao)s, %(cargo_id)s, %(comissao)s)"""
        )

        dados = {
            "nome": funcionario.nome,
            "CPF": funcionario.CPF,
            "data_admissao": funcionario.data_admissao,
            "cargo_id": funcionario.cargo_id,
            "comissao": funcionario.comissao
        }

        campos_info=[i for i in dados.values()]


        try:
            cursor.execute(adiciona_funcionario, dados)

        except IntegrityError:
            if int(funcionario.cargo_id) not in [10, 20, 30, 31, 32, 50]:
                raise InvalidFieldError("Id do cargo invalido.")
            else:
                raise DuplicatedCPF("CPF já cadastrado")
                
        except DatabaseError:
            if '' in campos_info or None in campos_info:
                raise EmptyFieldError('Campo do funcionario nao pode ser nulo ou vazio')
            else:
                raise InvalidFieldError('Dado de campo invalido')


        fecha_conexao(cnx,cursor)

    def consultar(self, cpf: str) -> Funcionario:

        cnx = conectar()

        cursor = cnx.cursor()
        query = (
            '''SELECT  CPF FROM xpto_alimentos.funcionario ''')

        cursor.execute(query)

        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))
        cursor.close()
        cursor = cnx.cursor()

        if cpf in cpf_list:
            query = ('''SELECT matricula,nome, CPF, data_admissao, cargo_id, comissao 
            FROM funcionario WHERE CPF=%s''')
            cursor.execute(query, [cpf])
            for (matricula,nome, cpf, data_admissao, cargo_id, comissao) in cursor:
                funcionario = Funcionario(
                    nome, cpf, data_admissao, cargo_id, comissao,matricula)
        else:
            cursor.close()
            cnx.close()
            raise FuncionarioNotFoundError("CPF não encontrado.")

        fecha_conexao(cnx,cursor)

        return funcionario

    def excluir(self, cpf: str) -> None:

        cnx = conectar()

        cursor = cnx.cursor()

        deleta_funcionario = (
            '''DELETE FROM funcionario 
        WHERE CPF = %s'''
        )
        cursor.execute('''SELECT CPF 
        FROM xpto_alimentos.funcionario''')
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))
        
        if cpf in cpf_list:
            cursor.execute(deleta_funcionario, (cpf,))    
        else:
            cursor.close()
            cnx.close()
            raise FuncionarioNotFoundError("CPF não encontrado.")

        fecha_conexao(cnx,cursor)

    def alterar_cadastro(self, cpf: str) -> None:

        cnx = conectar()

        cursor = cnx.cursor()

        # Listagem de cpf no database
        cursor.execute('''SELECT CPF 
        FROM xpto_alimentos.funcionario''')
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        if cpf in cpf_list:
            for i in range(len(self.__campos)):
                print(f"{i}----{self.__campos[i]}")

            index = int(input('Informe o codigo do campo a ser alterado:'))

            if index not in range(len(self.__campos)):
                print('codigo de campo nao existe')
            else:
                alteraçao = input('Nova info:\n')

            if alteraçao == None or alteraçao.isspace() or alteraçao == '':
                print('novo dado nao pode ser vazio')
            else:
                if "s" == input(f'Deseja alterar {self.__campos[index]} para "{alteraçao}"?(s/n) '):
                    sql = "UPDATE funcionario SET " + \
                        self.__campos[index]+" = %s WHERE CPF = %s"
                    cursor.execute(sql, (alteraçao, cpf))
                    cnx.commit()
                    print("alteracao feita")
        else:
            raise FuncionarioNotFoundError("CPF não encontrado.")


        fecha_conexao(cnx,cursor)

    def listar_funcionarios(self) -> list:

        cnx = conectar()
        
        cursor = cnx.cursor()

        lista_funcionarios = (
            '''SELECT CPF 
        FROM xpto_alimentos.funcionario'''
        )
        cursor.execute(lista_funcionarios)
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        if cpf_list== []:
            cursor.close()
            cnx.close()
            raise EmptyDataBaseError("Nao tem funcionarios cadastrados.")

        else:
            funcionarios_list=[]
            for cpf in cpf_list:
                funcionario=self.consultar(cpf)

                funcionarios_list.append(funcionario)

            funcionario_data={
                    'Matricula':[f.matricula for f in funcionarios_list],
                    'Nome':[f.nome for f in funcionarios_list],
                    'CPF':[f.CPF for f in funcionarios_list],
                    'Data de admissao':[f.data_admissao for f in funcionarios_list],
                    'Cargo':[f.cargo().descricao for f in funcionarios_list]
                        }

            df=pandas.DataFrame(funcionario_data)

            print(tabulate(df, headers='keys', tablefmt='psql'))

    
        fecha_conexao(cnx,cursor)

        return funcionarios_list
