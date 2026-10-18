class ControllerCliente:
    def cliente_existe(self, conexao, cpf):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM CLIENTES WHERE CPF = :1", (cpf,))
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    def total_registros(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM CLIENTES")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def listar(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT CPF, NOME, TELEFONE FROM CLIENTES ORDER BY NOME"
            )
            resultados = cursor.fetchall()
        finally:
            cursor.close()

        print("\n--- LISTA DE CLIENTES ---")
        if not resultados:
            print("Nenhum cliente cadastrado.")
        for cpf, nome, telefone in resultados:
            print(f"CPF: {cpf} | Nome: {nome} | Tel.: {telefone or '-'}")
        return resultados

    def inserir(self, conexao, cliente):
        cpf = cliente.get_cpf().strip()
        nome = cliente.get_nome().strip()
        telefone = cliente.get_telefone().strip() or None
        if len(cpf) != 11 or not cpf.isdigit():
            print("\n[!] O CPF deve conter exatamente 11 números.")
            return False
        if not nome:
            print("\n[!] O nome é obrigatório.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO CLIENTES (CPF, NOME, TELEFONE) VALUES (:1, :2, :3)",
                (cpf, nome, telefone),
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

    def atualizar(self, conexao, cpf_atual, cliente):
        cpf_novo = cliente.get_cpf().strip()
        nome = cliente.get_nome().strip()
        telefone = cliente.get_telefone().strip() or None
        if len(cpf_novo) != 11 or not cpf_novo.isdigit():
            print("\n[!] O CPF deve conter exatamente 11 números.")
            return False
        if not nome:
            print("\n[!] O nome é obrigatório.")
            return False
        if not self.cliente_existe(conexao, cpf_atual):
            print(f"\n[!] Cliente com CPF {cpf_atual} não existe.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(1) FROM LOCACOES WHERE CPF = :1",
                (cpf_atual,),
            )
            possui_locacoes = cursor.fetchone()[0] > 0
            if possui_locacoes and cpf_novo != cpf_atual:
                print("\n[!] Não é possível alterar o CPF de um cliente com locações.")
                return False
            cursor.execute(
                "UPDATE CLIENTES SET CPF = :1, NOME = :2, TELEFONE = :3 "
                "WHERE CPF = :4",
                (cpf_novo, nome, telefone, cpf_atual),
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

    def remover(self, conexao, cpf):
        if not self.cliente_existe(conexao, cpf):
            print(f"\n[!] Cliente com CPF {cpf} não encontrado.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM LOCACOES WHERE CPF = :1", (cpf,))
            possui_locacoes = cursor.fetchone()[0] > 0
            if possui_locacoes:
                print(f"\n[!] O cliente CPF {cpf} possui locações associadas.")
                confirmacao = input(
                    "Remover o cliente e TODAS as locações vinculadas? (S/N): "
                ).strip().upper()
                if confirmacao != "S":
                    conexao.rollback()
                    print("\n[-] Operação cancelada.")
                    return False
                cursor.execute("DELETE FROM LOCACOES WHERE CPF = :1", (cpf,))

            cursor.execute("DELETE FROM CLIENTES WHERE CPF = :1", (cpf,))
            conexao.commit()
            print("\n[+] Cliente removido com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível remover o cliente: {erro}")
            return False
        finally:
            cursor.close()
