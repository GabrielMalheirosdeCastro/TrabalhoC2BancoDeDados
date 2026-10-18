# Sistema de Locação de Veículos com Python e Oracle

Aplicação de terminal para cadastrar clientes, carros e locações no Oracle Database.

## Esquema usado pela aplicação

O programa usa as tabelas `LABDATABASE.CLIENTES`, `LABDATABASE.CARROS` e `LABDATABASE.LOCACOES`, criadas por `TabelasSQL/create_tables.sql`.

- `CLIENTES`: CPF (chave primária), nome e telefone.
- `CARROS`: placa (chave primária), modelo, marca e valor da diária.
- `LOCACOES`: código gerado por sequence, datas de início e previsão, data efetiva de devolução (nula enquanto aberta), dias, valor total, CPF e placa.

## Configuração

1. Instale Python e o driver Oracle:

   ```powershell
   python -m pip install oracledb
   ```

2. Copie `src/conexion/passphrase/authentication.example.oracle` para `src/conexion/passphrase/authentication.oracle`. Edite o arquivo local para conter `usuario,senha` fornecidos para o Oracle. O arquivo real está no `.gitignore`; não o envie ao repositório.

3. A conexão está configurada para `localhost`, porta `1521`, serviço `XEPDB1`, com usuário no arquivo de credenciais. Ao rodar dentro da VM Oracle, `localhost` aponta para essa própria VM.

4. No Oracle SQL Developer conectado ao schema `LABDATABASE`, execute uma única vez `TabelasSQL/create_tables.sql`. Se as tabelas já existirem com `DATA_FIM_LOCACAO` obrigatória, em vez de recriar o esquema, execute:

   ```sql
   ALTER TABLE LABDATABASE.LOCACOES MODIFY DATA_FIM_LOCACAO NULL;
   ```

5. Opcionalmente, execute `TabelasSQL/inserirDados.sql` para carregar dados fictícios. Execute-o apenas uma vez ou após limpar os dados de exemplo, pois os CPFs e placas são chaves únicas.

6. Na raiz do projeto, inicie a aplicação:

   ```powershell
   python src/main.py
   ```

   No Windows, também pode usar `py src/main.py`.

## Funcionalidades

- CRUD de clientes identificados pelo CPF.
- CRUD de carros identificados pela placa.
- CRUD de locações identificadas pelo código gerado pela sequence Oracle.
- A data prevista de devolução é calculada com base na data de início e na quantidade de dias.
- A data efetiva fica vazia até ser registrada pela opção **Registrar devolução**.
- Relatório detalhado de locações e faturamento por modelo.
- Consultas parametrizadas com bind variables Oracle.

## Estrutura

- `TabelasSQL/create_tables.sql`: criação das tabelas, relacionamentos e sequence Oracle.
- `TabelasSQL/inserirDados.sql`: dados fictícios compatíveis com o esquema.
- `src/Classes`: modelos de cliente, carro e locação.
- `src/ControllerClasses`: operações CRUD.
- `src/conexion/passphrase`: modelo de credenciais Oracle; o arquivo real é local e ignorado pelo Git.
- `src/newConexao.py`: conexão Oracle.
- `src/Relatorios.py`: relatórios.
- `src/main.py`: menus e ponto de entrada.

## Observações

- CPF é armazenado como texto para preservar zeros à esquerda.
- A sequence `LABDATABASE.LOCACOES_CODIGO_LOCACAO_SEQ` é usada para gerar o código da locação.
- O script de criação não apaga tabelas existentes. Execute-o em um schema vazio; se o schema já tiver objetos, não o execute novamente.
- Teste em um banco de desenvolvimento antes de usar dados reais.

## Créditos

Projeto desenvolvido para a avaliação C2 da disciplina de Banco de Dados, baseado na estrutura do projeto [example_crud_oracle](https://github.com/howardroatti/example_crud_oracle) de Howard Roatti (licença MIT).

## Contato

- [GitHub](https://github.com/Ceasa20)
