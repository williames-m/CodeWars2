import sys,os,unittest
from unittest import main,TestCase
mypath=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(mypath)
print(mypath)
from src.entities.funcionario import Funcionario
from src.business.cadastro_funcionario import CadastroFuncionario
from src.business.cadastro_holerite import CadastroHolerite

cadastro = CadastroFuncionario()
cadastro_holerite=CadastroHolerite()

funcionario = Funcionario('Juliano Gomes', '11114311122', '2019-06-17', '32', 'Sim')



# funcionario1 = Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "32", "Sim")
# funcionario2 = Funcionario('Daiana Santana de Sousa', "11111111100", '2002-04-09', "30", 'Sim')
# cadastro.inserir(funcionario)
# # cadastro.inserir(funcionario2)

# cadastro_holerite.gerar_holerite("11111111100")

# cadastro_holerite.listar_holerites()

# cadastro.excluir('11114311122')
# cadastro.alterar_cadastro("11111111122")


