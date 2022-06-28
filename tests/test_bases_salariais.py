import sys,os,unittest
from unittest import main,TestCase
mypath=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(mypath)
from src.business.bases_salariais import INSS, IRRF
from src.entities.funcionario import Funcionario


class TestCalculoINSS(TestCase):

    def test_INSS_faixa3(self):
        funcionario = Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "32", "Sim")
        self.assertEqual((279.8, 0.12),INSS(funcionario))

    def test_IRRF_faixa3(self):
        funcionario= Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "32", "Nao")
        self.assertEqual((53.23, 0.275), IRRF(funcionario))

    def test_INSS_faixa4(self):
        funcionario= Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "20", "Sim")
        self.assertEqual((828.39, 0.14),INSS(funcionario))

    def test_IRRF_faixa4(self):
        funcionario = Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "20", "Nao")
        self.assertEqual((827.83, 0.275), IRRF(funcionario))
   
    def test_INSS_faixa5(self):
        funcionario= Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "10", "Sim")
        self.assertEqual((828.39, 0.14),INSS(funcionario))

    def test_IRRF_faixa5(self):
        funcionario = Funcionario("Ana Maria Silva", "11111111100", "2019-02-07", "10", "Sim")
        self.assertEqual((1707.83, 0.275), IRRF(funcionario))

if __name__=='__main__':
    unittest.main()
    