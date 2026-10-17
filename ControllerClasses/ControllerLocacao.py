class ControllerLocacao:
    def __init__(self):
        pass

    def locacao_existe(self, conexao, id_locacao):
        """Verifica se uma locação existe pelo ID"""
        cursor = conexao.cursor()
        sql = "SELECT COUNT(1) FROM locacao WHERE id_locacao = " + str(id_locacao)
        cursor.execute(sql)
        existe = cursor.fetchone()[0] > 0
        cursor.close()
        return existe

    def total_registros(self, conexao):
        """Contagem para Splash Screen"""
        cursor = conexao.cursor()
        sql = "SELECT COUNT(1) total_locacao FROM locacao"
        cursor.execute(sql)
        total = cursor.fetchone()[0]
        cursor.close()
        return total

    def listar(self, conexao):
        """Lista todas as tuplas com FKs associadas e valores"""
        cursor = conexao.cursor()
        sql = """
            SELECT l.id_locacao, c.nome, k.modelo, l.data_locacao, l.dias, l.valor_total
            FROM locacao l
            INNER JOIN cliente c ON l.id_cliente = c.id_cliente
            INNER JOIN carro k ON l.id_carro = k.id_carro
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()

        print("\n--- LISTA DE LOCAÇÕES ---")
        for row in resultados:
            print(f"ID Locação: {row[0]} | Cliente: {row[1]} | Carro: {row[2]} | Data: {row[3]} | Dias: {row[4]} | Total: R$ {row[5]}")
        return resultados

    def inserir(self, conexao, locacao):
        """Inserção de nova locação (Valida FKs antes de inserir)"""
        cursor = conexao.cursor()
        sql = "INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total) VALUES (" + str(locacao.get_cliente().get_id_cliente()) + ", " + str(locacao.get_carro().get_id_carro()) + ", '" + locacao.get_data_locacao() + "', " + str(locacao.get_dias()) + ", " + str(locacao.get_valor_total()) + ")"
        cursor.execute(sql)
        conexao.commit()
        cursor.close()
        print("\n[+] Locação registrada com sucesso!")

    def atualizar(self, conexao, locacao):
        """Atualização de locação existente"""
        if not self.locacao_existe(conexao, locacao.get_id_locacao()):
            print(f"\n[!] Erro: Locação com ID {locacao.get_id_locacao()} não existe.")
            return

        cursor = conexao.cursor()
        sql = "UPDATE locacao SET id_cliente = " + str(locacao.get_cliente().get_id_cliente()) + ", id_carro = " + str(locacao.get_carro().get_id_carro()) + ", data_locacao = '" + locacao.get_data_locacao() + "', dias = " + str(locacao.get_dias()) + ", valor_total = " + str(locacao.get_valor_total()) + " WHERE id_locacao = " + str(locacao.get_id_locacao())
        cursor.execute(sql)
        conexao.commit()
        cursor.close()
        print("\n[+] Locação atualizada com sucesso!")

    def remover(self, conexao, id_locacao):
        """Remoção de registro da tabela filha"""
        if not self.locacao_existe(conexao, id_locacao):
            print(f"\n[!] Erro: Locação com ID {id_locacao} não encontrada.")
            return

        cursor = conexao.cursor()
        sql = "DELETE FROM locacao WHERE id_locacao = " + str(id_locacao)
        cursor.execute(sql)
        conexao.commit()
        cursor.close()
        print("\n[+] Locação removida com sucesso!")