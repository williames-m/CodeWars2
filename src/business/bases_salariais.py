import sys,os
mypath=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(mypath)
from src.entities.funcionario import Funcionario

def INSS(funcionario:Funcionario)->float:
    salario_b=funcionario.cargo().salario_base
    salario=salario_b*(1+funcionario.cargo().comissao/100)

    faixas_INSS={(0,1212):0.075,
                    (1212.01,2427.35):0.09,
                    (2427.36,3641.03):0.12,
                    (3641.04,7087.22):0.14
                    }
    recolher=0
    for intervalo,aliquota in faixas_INSS.items():

        if not intervalo[0]<salario<intervalo[1]:#fora da faixa salarial
            recolher+=(intervalo[1]-intervalo[0])*aliquota
        else:
            if aliquota==0.075:#primeira faixa salarial
                recolher+=(intervalo[1]-salario)*aliquota
            else:
                recolher+=(salario-intervalo[0])*aliquota
            break

    return round(recolher,2),aliquota 

def IRRF(funcionario:Funcionario)->float:
    salario=funcionario.cargo().salario_base

    faixas_IRRF={(0,1903.98):(0,0),
                (1903.99,2826.65):(0.075,142.8),
                (2826.66,3751.05):(0.15,354.80),
                (3751.06,4664.68):(0.225,636.13),
                (4664.69,float('inf')):(0.275,869.36)
                }

    for intervalo,(aliquota,deducao) in faixas_IRRF.items():

        if intervalo[0]<salario<intervalo[1]:#fora da faixa do imposto de renda
            imposto=(salario-INSS(funcionario)[0])*aliquota-deducao
    
    return round(imposto,2),aliquota

