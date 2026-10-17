class ControllerCliente:
    def __init__(self):
        pass

    def cliente_existe(self, conexao, id_cliente):
        """Verifica se um cliente existe pelo ID"""
        cursor = conexao.cursor()
        sql = "SELECT COUNT(1) FROM cliente WHERE id_cliente = " + str(id_cliente)
        cursor.execute(sql)
        existe = cursor.fetchone()[0] > 0
        cursor.close()
        return existe

    def total_registros(self, conexao):
        """Contagem para Splash Screen"""
        cursor = conexao.cursor()
        sql = "SELECT COUNT(1) total_cliente FROM cliente"
        cursor.execute(sql)
        total = cursor.fetchone()[0]
        cursor.close()
        return total

    def listar(self, conexao):
        """Lista todas as tuplas com PK e campo descritivo (Item 6.c.3 / 6.d.3)"""
        cursor = conexao.cursor()
        sql = "SELECT id_cliente, nome, cpf, telefone FROM cliente"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()
        
        print("\n--- LISTA DE CLIENTES ---")
        for row in resultados:
            print(f"ID: {row[0]} | Nome: {row[1]} | CPF: {row[2]} | Tel: {row[3]}")
        return resultados

    def inserir(self, conexao, cliente):
        """Inserção de novo cliente (Item 6.b)"""
        cursor = conexao.cursor()
        sql = "INSERT INTO cliente (nome, cpf, telefone) VALUES ('" + cliente.get_nome() + "', '" + cliente.get_cpf() + "', '" + cliente.get_telefone() + "')"
        cursor.execute(sql)
        conexao.commit()
        cursor.close()
        print("\n[+] Cliente inserido com sucesso!")

    def atualizar(self, conexao, cliente):
        """Atualização de cliente existente (Item 6.d)"""
        if not self.cliente_existe(conexao, cliente.get_id_cliente()):
            print(f"\n[!] Erro: Cliente com ID {cliente.get_id_cliente()} não existe.")
            return

        cursor = conexao.cursor()
        sql = "UPDATE cliente SET nome = '" + cliente.get_nome() + "', cpf = '" + cliente.get_cpf() + "', telefone = '" + cliente.get_telefone() + "' WHERE id_cliente = " + str(cliente.get_id_cliente())
        cursor.execute(sql)
        conexao.commit()
        cursor.close()
        print("\n[+] Cliente atualizado com sucesso!")

    def remover(self, conexao, id_cliente):
        """Remoção de cliente com tratamento de FK (Item 6.c)"""
        if not self.cliente_existe(conexao, id_cliente):
            print(f"\n[!] Erro: Cliente com ID {id_cliente} não encontrado.")
            return

        cursor = conexao.cursor()

        # Verificação de Foreign Key em locacao (Item 6.c.5.i)
        sql_fk = "SELECT COUNT(1) FROM locacao WHERE id_cliente = " + str(id_cliente)
        cursor.execute(sql_fk)
        has_fk = cursor.fetchone()[0]

        if has_fk > 0:
            print(f"\n[!] Atenção: O cliente ID {id_cliente} possui locações associadas!")
            confirmacao = input("Deseja remover o cliente E TODAS as suas locações vinculadas? (S/N): ")
            if confirmacao.upper() == 'S':
                sql_del_filha = "DELETE FROM locacao WHERE id_cliente = " + str(id_cliente)
                cursor.execute(sql_del_filha)
            else:
                print("\n[-] Operação cancelada.")
                cursor.close()
                return

        sql_del_pai = "DELETE FROM cliente WHERE id_cliente = " + str(id_cliente)
        cursor.execute(sql_del_pai)
        conexao.commit()
        cursor.close()
        print("\n[+] Cliente removido com sucesso!")