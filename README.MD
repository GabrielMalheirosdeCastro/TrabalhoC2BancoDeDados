# Sistema de Locação de Veículos

Aplicação de terminal desenvolvida em Python para administrar clientes, veículos e locações usando MySQL. O sistema implementa operações CRUD e relatórios com consultas `JOIN`, `GROUP BY`, `COUNT` e `SUM`.

> **Importante:** o grupo está trabalhando na unificação do banco de dados. Antes de executar os arquivos SQL ou alterar o nome do banco na aplicação, confirme com os responsáveis qual será o esquema definitivo. Os arquivos Python atuais esperam as tabelas `cliente`, `carro` e `locacao` descritas abaixo.

## Funcionalidades

- Cadastro, listagem, atualização e remoção de clientes.
- Cadastro, listagem, atualização e remoção de veículos.
- Registro, listagem, atualização e remoção de locações.
- Confirmação antes de excluir registros.
- Exclusão transacional das locações associadas quando o usuário confirma a exclusão de um cliente ou veículo.
- Relatório detalhado de locações com `JOIN`.
- Relatório de faturamento por modelo com agregação.
- Validação de entradas numéricas, datas, campos obrigatórios e valores de diária.
- Consultas parametrizadas para reduzir riscos de SQL injection e problemas com aspas nos dados.

## Tecnologias

- Python 3.10 ou superior (recomendado).
- MySQL.
- MySQL Connector/Python.

## Estrutura do projeto

```text
.
├── Diagramas_Relacionais/
├── TabelasSQL/
│   └── create_tables.sql
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

## Instalação

1. Instale Python e MySQL.
2. Na raiz do projeto, crie e ative um ambiente virtual (opcional, mas recomendado):

   **Windows**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux/macOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instale o conector:
   ```bash
   python -m pip install mysql-connector-python
   ```

4. Configure usuário, senha e banco no arquivo `src/main.py` (objeto `Conexao`) e confirme que o arquivo `src/Conexao.py` está consistente com essa configuração. Não publique senhas reais no repositório.

## Banco de dados

O sistema Python espera estas tabelas e colunas:

- `cliente`: `id_cliente`, `nome`, `cpf`, `telefone`
- `carro`: `id_carro`, `modelo`, `marca`, `placa`, `valor_diaria`
- `locacao`: `id_locacao`, `id_cliente`, `id_carro`, `data_locacao`, `dias`, `valor_total`

As tabelas devem ter chaves primárias e relacionamentos entre `locacao.id_cliente` e `cliente.id_cliente`, e entre `locacao.id_carro` e `carro.id_carro`.

O arquivo `TabelasSQL/create_tables.sql` existente pode estar em uma versão de esquema diferente da esperada pelo Python. **Não execute esse script sem confirmar a versão final com o grupo**, pois a unificação do banco está em andamento.

Para inserir registros de demonstração, consulte `TabelasSQL/sample_data.sql`. Esse script foi escrito para o esquema listado acima e deve ser usado somente depois que o esquema final for confirmado e o banco estiver vazio ou após revisão dos dados que já existem.

## Execução

A partir da raiz do projeto:

```bash
python src/main.py
```

Se o comando `python` não estiver disponível no ambiente, tente `py src/main.py` no Windows ou `python3 src/main.py` no Linux/macOS.

## Dados de demonstração

O arquivo `TabelasSQL/sample_data.sql` contém clientes, carros e locações de exemplo. Execute-o no banco MySQL somente após confirmar que as tabelas possuem as colunas esperadas. Os registros de exemplo usam CPF e placa próprios para facilitar a identificação; revise antes de importar para um banco que já contenha dados.

## Observações

- As datas solicitadas pelo programa são informadas no formato `DD/MM/AAAA`.
- O valor total da locação é calculado a partir do valor atual da diária multiplicado pela quantidade de dias.
- O nome do banco configurado no ponto de entrada deve coincidir com o nome usado na conexão. Essa configuração deve ser alinhada com a decisão do grupo sobre a unificação.
- Teste as operações em um banco de desenvolvimento antes de usar dados reais.
