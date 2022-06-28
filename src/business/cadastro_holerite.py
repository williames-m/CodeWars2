#==================external modules=====================
import pandas
from tabulate import tabulate
import calendar

import os,sys

mypath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(mypath)

from mysql.connector.errors import IntegrityError,DatabaseError
from src.entities.holerites import Holerite
from src.business.cadastro_funcionario import CadastroFuncionario
from src.business.access_data_base import conectar, fecha_conexao
from src.exception.base_funcionario_error import EmptyDataBaseError
from src.business.bases_salariais import INSS, IRRF
from src.exception.field_error import InvalidFieldError

class CadastroHolerite():

    def listar_holerites(self):

        cnx = conectar()

        cursor = cnx.cursor()

        query=("""SELECT CPF FROM funcionario 
                                WHERE CPF NOT IN (SELECT funcionario_CPF FROM holerite where mes=%s  )""")

    
        mes_referencia=int(input('informe o mes do holerite(em numero)'))
        cursor.execute(query, (mes_referencia,))
        
        cpf_list = list(map(lambda x: x[0], cursor.fetchall()))

        if cpf_list == []:
            raise EmptyDataBaseError('Não há CPFs cadastrados na base de dados.')
        
        cursor.close()

        holerite_list=[Holerite(cpf,mes_referencia) for cpf in cpf_list]
        
        for holerite in holerite_list:
            (inss, irrf, FGTS_do_mes, a_receber) = print_holerite(holerite)
            print('\n')
            print('\n')

            cursor = cnx.cursor()
            adiciona_holerite = (
                """INSERT INTO holerite
                (funcionario_CPF,mes,faltas, INSS, IRRF, FGTS, valor_recebido) 
                VALUES ( %(funcionario_CPF)s, %(mes)s, %(faltas)s, %(INSS)s, %(IRRF)s, %(FGTS)s, %(valor_recebido)s)"""
            )

            dados = {
                "funcionario_CPF": holerite.cpf,
                "mes": holerite.mes_referencia,
                "faltas": holerite.faltas,
                "INSS": inss,
                "IRRF": irrf,
                "FGTS": FGTS_do_mes,
                "valor_recebido": a_receber,
            }
        
            cursor.execute(adiciona_holerite, dados)
            cnx.commit()

            cursor.close()

        fecha_conexao(cnx,cursor)

        pass

    def gerar_holerite(self,cpf:str):

        cnx = conectar()
                              
        cursor = cnx.cursor(buffered=True)

        funcionario=CadastroFuncionario().consultar(cpf)

        mes_referencia=int(input('informe o mes do holerite(em numero)'))
        
        if not 0<mes_referencia<13: 
            cursor.close()
            cnx.close()
            raise InvalidFieldError(f"mes {calendar.month_name[mes_referencia]} nao é valido")

        faltas=int(input('quantas faltas?'))
        holerite=Holerite(cpf,mes_referencia,faltas)
        
        (inss, irrf, FGTS_do_mes, a_receber) = print_holerite(holerite)
        

        adiciona_holerite = (
            """INSERT INTO holerite
            (funcionario_CPF,mes,faltas, INSS, IRRF, FGTS, valor_recebido) 
            VALUES ( %(funcionario_CPF)s, %(mes)s, %(faltas)s, %(INSS)s, %(IRRF)s, %(FGTS)s, %(valor_recebido)s)"""
        )

        dados = {
            "funcionario_CPF": holerite.cpf,
            "mes": holerite.mes_referencia,
            "faltas": holerite.faltas,
            "INSS": inss,
            "IRRF": irrf,
            "FGTS": FGTS_do_mes,
            "valor_recebido": a_receber,
        }

        try:
            cursor.execute(adiciona_holerite, dados)
            cnx.commit()
        except IntegrityError:
            print(f'O funcionario {funcionario.nome} ja tem as faltas no mes {calendar.month_name[mes_referencia]} registradas')
            cursor.close()
            cnx.close()
            exit()
        
            
        fecha_conexao(cnx,cursor)
        pass

        
def print_holerite(holerite:Holerite):
    # =================Print Holerite========================== 
    funcionario=holerite.funcionario()    
    salario_base=funcionario.cargo().salario_base

    if funcionario.comissao=='Sim':
        comissao=funcionario.cargo().comissao
    else:
        comissao=0

    inss,aliquota_inss = INSS(funcionario)
    irrf,aliquota_irrf = IRRF(funcionario)
    valor_comissao = comissao *  salario_base/100
    Base_calc_INSS = salario_base + valor_comissao
    desconto_faltas = salario_base/30*holerite.faltas
    FGTS_do_mes = Base_calc_INSS * 0.08
    Base_calc_IRRF = Base_calc_INSS - inss
    total_descontos = desconto_faltas + inss + irrf
    a_receber = Base_calc_INSS - total_descontos

     
    funcionario_data={
        'Matricula':[funcionario.matricula],
        'Nome':[funcionario.nome],
        'CPF':[funcionario.CPF],
        'Data de admissao':[funcionario.data_admissao],
        'Cargo':[funcionario.cargo().descricao]
    }

    df=pandas.DataFrame(funcionario_data)
    print(tabulate(df, headers='keys', tablefmt='psql'))


    print(f'=========={calendar.month_name[holerite.mes_referencia]}/2022========')

    holerite_data = {
        'Descrição': ['Salário Base','Comissão', 'Faltas', 'INSS Folha', 'IRRF Folha', 'Total', 'liq. a receber'],
        'Referência': ['22,5', comissao, holerite.faltas, aliquota_inss, aliquota_irrf, '    ', '    '],
        'Provento': [salario_base, valor_comissao, '    ', '    ','   ', Base_calc_INSS, a_receber],
        'Desconto': ['    ', '    ',desconto_faltas, inss, irrf, total_descontos,'    '],
        }

    df2=pandas.DataFrame(holerite_data)
    print(tabulate(df2, headers='keys', tablefmt='psql'))
    
    impostos_data = {
        'Base calc INSS': [Base_calc_INSS],
        'Base calc FGTS': [Base_calc_INSS],
        'FGTS do mês': [FGTS_do_mes],
        'Base calc IRRF': [Base_calc_IRRF]
    }

    df3=pandas.DataFrame(impostos_data)
    print(tabulate(df3, headers='keys', tablefmt='psql'))

    return (inss, irrf, FGTS_do_mes, a_receber)
    