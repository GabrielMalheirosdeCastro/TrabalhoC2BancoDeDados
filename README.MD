# Sistema de Locação de Veículos em Python com CRUD no MySQL

Esse sistema é composto por um conjunto de tabelas que representam a locação de veículos, contendo as tabelas: **cliente**, **carro** e **locacao**.

O sistema exige que as tabelas existam, então basta executar o script SQL de criação das tabelas (e, opcionalmente, o de dados de exemplo) diretamente no MySQL:

```
mysql -u <usuario> -p <nome_do_banco> < TabelasSQL/create_tables.sql
mysql -u <usuario> -p <nome_do_banco> < TabelasSQL/sample_data.sql
```

Para executar o sistema basta executar o script Python a seguir, a partir da raiz do projeto:

```
python src/main.py
```

> Se o comando `python` não estiver disponível, use `py src/main.py` no Windows ou `python3 src/main.py` no Linux/macOS.

> **Importante:** o grupo está trabalhando na unificação do banco de dados. Antes de executar os arquivos SQL ou alterar o nome do banco na aplicação, confirme com os responsáveis qual será o esquema definitivo. Os arquivos Python atuais esperam as tabelas `cliente`, `carro` e `locacao` descritas abaixo.

## Funcionalidades

- Cadastro, listagem, atualização e remoção de clientes.
- Cadastro, listagem, atualização e remoção de veículos.
- Registro, listagem, atualização e remoção de locações.
- Confirmação antes de excluir registros.
- Exclusão transacional das locações associadas quando o usuário confirma a exclusão de um cliente ou veículo.
- Relatório detalhado de locações com `JOIN`.
- Relatório de faturamento por modelo com agregação (`GROUP BY`, `COUNT` e `SUM`).
- Validação de entradas numéricas, datas, campos obrigatórios e valores de diária.
- Consultas parametrizadas para reduzir riscos de SQL injection e problemas com aspas nos dados.

## Tecnologias

- Python 3.10 ou superior (recomendado)
- MySQL
- MySQL Connector/Python

## Organização

- [Diagramas_Relacionais](Diagramas_Relacionais): Nesse diretório está o diagrama relacional (lógico) do sistema.
  * O sistema possui três entidades: **CLIENTE**, **CARRO** e **LOCACAO**.
- [TabelasSQL](TabelasSQL): Nesse diretório estão os scripts para criação das tabelas e inserção de dados fictícios para testes do sistema.
  * [create_tables.sql](TabelasSQL/create_tables.sql): script responsável pela criação das tabelas e relacionamentos.
  * [sample_data.sql](TabelasSQL/sample_data.sql): script responsável pela inserção dos registros fictícios (clientes, carros e locações) para testes do sistema.
  * Os registros de exemplo usam CPF e placa próprios para facilitar a identificação; revise antes de importar para um banco que já contenha dados.
- [src](src): Nesse diretório estão os scripts do sistema.
  * [Classes](src/Classes): Classes das entidades descritas no diagrama relacional (`Cliente.py`, `Carro.py` e `Locacao.py`).
  * [ControllerClasses](src/ControllerClasses): Classes controladoras, responsáveis por realizar inserção, alteração, listagem e exclusão dos registros das tabelas (`ControllerCliente.py`, `ControllerCarro.py` e `ControllerLocacao.py`).
  * [Conexao.py](src/Conexao.py): Módulo de conexão com o banco de dados MySQL, com funcionalidades para execução de instruções de consulta e alteração.
  * [Relatorios.py](src/Relatorios.py): Classe responsável por gerar os relatórios do sistema (locações detalhadas e faturamento por modelo).
  * [main.py](src/main.py): Script responsável por ser a interface entre o usuário e os módulos de acesso ao banco de dados. Deve ser executado após a criação das tabelas.

```
.
├── Diagramas_Relacionais/
├── TabelasSQL/
│   ├── create_tables.sql
│   └── sample_data.sql
├── src/
│   ├── Classes/
│   │   ├── Carro.py
│   │   ├── Cliente.py
│   │   └── Locacao.py
│   ├── ControllerClasses/
│   │   ├── ControllerCarro.py
│   │   ├── ControllerCliente.py
│   │   └── ControllerLocacao.py
│   ├── Conexao.py
│   ├── Relatorios.py
│   └── main.py
└── README.MD
```

## Banco de dados

O sistema Python espera estas tabelas e colunas:

| Tabela    | Colunas                                                                  |
| --------- | ------------------------------------------------------------------------ |
| `cliente` | `id_cliente`, `nome`, `cpf`, `telefone`                                  |
| `carro`   | `id_carro`, `modelo`, `marca`, `placa`, `valor_diaria`                   |
| `locacao` | `id_locacao`, `id_cliente`, `id_carro`, `data_locacao`, `dias`, `valor_total` |

As tabelas devem ter chaves primárias e relacionamentos entre `locacao.id_cliente` e `cliente.id_cliente`, e entre `locacao.id_carro` e `carro.id_carro`.

O arquivo `TabelasSQL/create_tables.sql` pode estar em uma versão de esquema diferente da esperada pelo Python. **Não execute esse script sem confirmar a versão final com o grupo**, pois a unificação do banco está em andamento.

## Instalação

1. Instale Python e MySQL.

2. Na raiz do projeto, crie e ative um ambiente virtual (opcional, mas recomendado):

   **Windows**

   ```
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux/macOS**

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale o conector:

   ```
   python -m pip install mysql-connector-python
   ```

4. Configure usuário, senha e banco no arquivo `src/main.py` (objeto `Conexao`) e confirme que o arquivo `src/Conexao.py` está consistente com essa configuração. **Não publique senhas reais no repositório.**

## Observações

- As datas solicitadas pelo programa são informadas no formato `DD/MM/AAAA`.
- O valor total da locação é calculado a partir do valor atual da diária multiplicado pela quantidade de dias.
- O nome do banco configurado no ponto de entrada deve coincidir com o nome usado na conexão. Essa configuração deve ser alinhada com a decisão do grupo sobre a unificação.
- Teste as operações em um banco de desenvolvimento antes de usar dados reais.

## Créditos

Projeto desenvolvido para a avaliação C2 da disciplina de Banco de Dados, baseado na estrutura do projeto [example_crud_oracle](https://github.com/howardroatti/example_crud_oracle) de Howard Roatti (licença MIT).

## Contato

- [GitHub](https://github.com/Ceasa20)
