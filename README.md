
# Code-Wars-II
___

## Projeto em equipe do Bootcamp Código[s] - Stone

#### Equipe 10

* Lígia de Oliveira
* Marcelo Lopes Valerio
* William Machado
* Larissa Chagas
* Lucas Valença
  
<h3 align="left"> Modulos externos usados </h3>

* tabulate
* pandas
* mysql

<h2 align="left"> Tabela de conteudo </h2>

  - [Definições do Projeto](#Definições-do-Projeto)
  - [Organizaçao Base de Dados](#Organizaçao-Base-de-Dados)
  - [Codigo](#Codigo)
  
### Definições do Projeto

Implementar um sistema em python que cadastre holerites de funcionários, apresentando, para cada mês registrado, faltas, salário, comissão, e calculando descontos como INSS e IRRF. Após isso, salvá-las em um banco de dados MySQL, que possua informações sobre os cargos da empresa, e dos funcionários, além de permitir a alteração dos dados dos funcionários.

O programa possui como entrada as seguintes informações do funcionário: CPF, nome, data de admissão, código do cargo, e se ele recebe ou não a comissão, e, de acordo com as requisições do usuário, pode realizar alterações na base de dados, linkar dados de cargo com funcionário, e alterar o cargo do funcionário, por exemplo. Além disso, pode printar, no terminal python, uma holerite com os dados esquematizados. O programa gera automaticamente um numero de matricula para funcionários cadastrados,
servindo como chave primária para o MySQL

### Base de Dados 

**Para rodar o sistema, primeiramente é necessario gerar a base de dados, rodando o código disponibilizado na pasta SQL, e, após isso, colocar o cadastro do seu SQL na função conectar().**

_Inicialmente na base de dados nao existe nenhum funcionario ou holerite cadastrado somente as informações dos cargos disponiveis_ 

A organização do codigo e da base de dados encontras-se representados nas imagens abaixo

<p align="center">
<a><img src=https://user-images.githubusercontent.com/86573930/176080165-9f4ff77a-ca42-4591-a1a3-0258e90b6631.png  width="400px" ></a>
</p>
<p align="center">
<a><img src=https://user-images.githubusercontent.com/86573930/176080180-2adc5926-0874-4500-b8c2-629ed99434cc.PNG  width="400px" ></a>
</p>

### Codigo

#### Gerar Holerite(cpf)
Gera o holerite para um funcionario especifico (identificado pelo cpf) a partir da entrada do mes e da informação das faltas , desdeque ja nao exista um holerite cadastrado para esse funcionario no mes fornecido
- input
````
cadastro = CadastroFuncionario()
cadastro_holerite=CadastroHolerite()
funcionario = Funcionario('Daiana Santana de Sousa', "11111111100", '2002-04-09', "30", 'Sim')
cadastro.inserir(funcionario)
cadastro_holerite.gerar_holerite("11111111100")
````
-  output terminal
````
informe o mes do holerite(em numero)5
quantas faltas?2

+----+-------------+-------------------------+-------------+--------------------+-----------------------------+
|    |   Matricula | Nome                    |         CPF | Data de admissao   | Cargo                       |
|----+-------------+-------------------------+-------------+--------------------+-----------------------------|
|  0 |      100047 | Daiana Santana de Sousa | 11111111100 | 2002-04-09         | Desenvolvedor Mobile Sênior |
+----+-------------+-------------------------+-------------+--------------------+-----------------------------+
==========May/2022========
+----+----------------+--------------+-------------------+--------------------+
|    | Descrição      | Referência   | Provento          | Desconto           |
|----+----------------+--------------+-------------------+--------------------|
|  0 | Salário Base   | 22,5         | 6700.0            |                    |
|  1 | Comissão       | 7.0          | 469.0             |                    |
|  2 | Faltas         | 2            |                   | 446.6666666666667  |
|  3 | INSS Folha     | 0.14         |                   | 828.39             |
|  4 | IRRF Folha     | 0.275        |                   | 745.33             |
|  5 | Total          |              | 7169.0            | 2020.3866666666668 |
|  6 | liq. a receber |              | 5148.613333333333 |                    |
+----+----------------+--------------+-------------------+--------------------+
+----+------------------+------------------+---------------+------------------+
|    |   Base calc INSS |   Base calc FGTS |   FGTS do mês |   Base calc IRRF |
|----+------------------+------------------+---------------+------------------|
|  0 |             7169 |             7169 |        573.52 |          6340.61 |
+----+------------------+------------------+---------------+------------------+
````

#### Listar Holerites()
Se, apos rodar a funcao acima, requisitar a geracao da listagem dos holerittes para o mes 5 somente serao listados o holerite para o segundo funcionario fornecido ja que o primeiro ja teve seu holerite feito para aquele mes.

- input
  ````
  funcionario2 = Funcionario('Juliano Gomes', '11114311122', '2019-06-17', '32', 'Sim')
  cadastro.inserir(funcionario2)
  cadastro_holerite.listar_holerites()
  ````
  
-  output terminal
````
informe o mes do holerite(em numero)5
+----+-------------+---------------+-------------+--------------------+----------------------+
|    |   Matricula | Nome          |         CPF | Data de admissao   | Cargo                |
|----+-------------+---------------+-------------+--------------------+----------------------|
|  0 |      100049 | Juliano Gomes | 11114311122 | 2019-06-17         | Desenvolvedor Junior |
+----+-------------+---------------+-------------+--------------------+----------------------+
==========May/2022========
+----+----------------+--------------+------------+--------------------+
|    | Descrição      | Referência   | Provento   | Desconto           |
|----+----------------+--------------+------------+--------------------|
|  0 | Salário Base   | 22,5         | 3000.0     |                    |
|  1 | Comissão       | 3.0          | 90.0       |                    |
|  2 | Faltas         | 0            |            | 0.0                |
|  3 | INSS Folha     | 0.12         |            | 279.8              |
|  4 | IRRF Folha     | 0.275        |            | 53.23              |
|  5 | Total          |              | 3090.0     | 333.03000000000003 |
|  6 | liq. a receber |              | 2756.97    |                    |
+----+----------------+--------------+------------+--------------------+
+----+------------------+------------------+---------------+------------------+
|    |   Base calc INSS |   Base calc FGTS |   FGTS do mês |   Base calc IRRF |
|----+------------------+------------------+---------------+------------------|
|  0 |             3090 |             3090 |         247.2 |           2810.2 |
+----+------------------+------------------+---------------+------------------+
````

#### Listar_Funcionarios()

Lista os funcionarios presentes na base de dados 

````
+----+-------------+-------------------------+-------------+--------------------+-----------------------------+
|    |   Matricula | Nome                    |         CPF | Data de admissao   | Cargo                       |
|----+-------------+-------------------------+-------------+--------------------+-----------------------------|
|  0 |      100047 | Daiana Santana de Sousa | 11111111100 | 2002-04-09         | Desenvolvedor Mobile Sênior |
|  1 |      100049 | Juliano Gomes           | 11114311122 | 2019-06-17         | Desenvolvedor Junior        |
+----+-------------+-------------------------+-------------+--------------------+-----------------------------+
````
