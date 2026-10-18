class ControllerCliente:
    def cliente_existe(self, conexao, id_cliente):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(1) FROM cliente WHERE id_cliente = %s",
                (id_cliente,),
            )
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    def total_registros(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM cliente")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def listar(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT id_cliente, nome, cpf, telefone FROM cliente ORDER BY nome"
            )
            resultados = cursor.fetchall()
        finally:
            cursor.close()

        print("\n--- LISTA DE CLIENTES ---")
        if not resultados:
            print("Nenhum cliente cadastrado.")
        for row in resultados:
            print(f"ID: {row[0]} | Nome: {row[1]} | CPF: {row[2]} | Tel.: {row[3]}")
        return resultados

    def inserir(self, conexao, cliente):
        dados = (
            cliente.get_nome().strip(),
            cliente.get_cpf().strip(),
            cliente.get_telefone().strip(),
        )
        if not all(dados):
            print("\n[!] Nome, CPF e telefone são obrigatórios.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO cliente (nome, cpf, telefone) VALUES (%s, %s, %s)",
                dados,
            )
            conexao.commit()
            print("\n[+] Cliente inserido com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível inserir o cliente: {erro}")
            return False
        finally:
            cursor.close()

    def atualizar(self, conexao, cliente):
        id_cliente = cliente.get_id_cliente()
        dados = (
            cliente.get_nome().strip(),
            cliente.get_cpf().strip(),
            cliente.get_telefone().strip(),
        )
        if not all(dados):
            print("\n[!] Nome, CPF e telefone são obrigatórios.")
            return False
        if not self.cliente_existe(conexao, id_cliente):
            print(f"\n[!] Cliente com ID {id_cliente} não existe.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "UPDATE cliente SET nome = %s, cpf = %s, telefone = %s "
                "WHERE id_cliente = %s",
                (*dados, id_cliente),
            )
            conexao.commit()
            print("\n[+] Cliente atualizado com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível atualizar o cliente: {erro}")
            return False
        finally:
            cursor.close()

    def remover(self, conexao, id_cliente):
        if not self.cliente_existe(conexao, id_cliente):
            print(f"\n[!] Cliente com ID {id_cliente} não encontrado.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(1) FROM locacao WHERE id_cliente = %s",
                (id_cliente,),
            )
            possui_locacoes = cursor.fetchone()[0] > 0

            if possui_locacoes:
                print(f"\n[!] O cliente ID {id_cliente} possui locações associadas.")
                confirmacao = input(
                    "Remover o cliente e TODAS as locações vinculadas? (S/N): "
                ).strip().upper()
                if confirmacao != "S":
                    conexao.rollback()
                    print("\n[-] Operação cancelada.")
                    return False
                cursor.execute("DELETE FROM locacao WHERE id_cliente = %s", (id_cliente,))

            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
            conexao.commit()
            print("\n[+] Cliente removido com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível remover o cliente: {erro}")
            return False
        finally:
            cursor.close()
