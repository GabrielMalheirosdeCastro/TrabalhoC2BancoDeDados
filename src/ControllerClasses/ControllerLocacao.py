class ControllerLocacao:
    def locacao_existe(self, conexao, id_locacao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM locacao WHERE id_locacao = %s", (id_locacao,))
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    def total_registros(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM locacao")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def listar(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                SELECT l.id_locacao, c.nome, k.modelo, l.data_locacao,
                       l.dias, l.valor_total
                FROM locacao l
                INNER JOIN cliente c ON l.id_cliente = c.id_cliente
                INNER JOIN carro k ON l.id_carro = k.id_carro
                ORDER BY l.data_locacao DESC, l.id_locacao DESC
                """
            )
            resultados = cursor.fetchall()
        finally:
            cursor.close()

        print("\n--- LISTA DE LOCAÇÕES ---")
        if not resultados:
            print("Nenhuma locação cadastrada.")
        for row in resultados:
            print(
                f"ID: {row[0]} | Cliente: {row[1]} | Carro: {row[2]} | "
                f"Data: {row[3]} | Dias: {row[4]} | Total: R$ {float(row[5]):.2f}"
            )
        return resultados

    def inserir(self, conexao, locacao):
        try:
            dias = int(locacao.get_dias())
            total = float(locacao.get_valor_total())
            id_cliente = int(locacao.get_cliente().get_id_cliente())
            id_carro = int(locacao.get_carro().get_id_carro())
        except (TypeError, ValueError, AttributeError):
            print("\n[!] Dados inválidos para registrar a locação.")
            return False

        if dias <= 0 or total < 0:
            print("\n[!] Dias devem ser maiores que zero e o total não pode ser negativo.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO locacao (id_cliente, id_carro, data_locacao, dias, valor_total) "
                "VALUES (%s, %s, %s, %s, %s)",
                (id_cliente, id_carro, locacao.get_data_locacao(), dias, total),
            )
            conexao.commit()
            print("\n[+] Locação registrada com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível registrar a locação: {erro}")
            return False
        finally:
            cursor.close()

    def atualizar(self, conexao, locacao):
        id_locacao = locacao.get_id_locacao()
        if not self.locacao_existe(conexao, id_locacao):
            print(f"\n[!] Locação com ID {id_locacao} não existe.")
            return False
        try:
            dias = int(locacao.get_dias())
            total = float(locacao.get_valor_total())
            id_cliente = int(locacao.get_cliente().get_id_cliente())
            id_carro = int(locacao.get_carro().get_id_carro())
        except (TypeError, ValueError, AttributeError):
            print("\n[!] Dados inválidos para atualizar a locação.")
            return False
        if dias <= 0 or total < 0:
            print("\n[!] Dias devem ser maiores que zero e o total não pode ser negativo.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                UPDATE locacao
                SET id_cliente = %s, id_carro = %s, data_locacao = %s,
                    dias = %s, valor_total = %s
                WHERE id_locacao = %s
                """,
                (
                    id_cliente, id_carro, locacao.get_data_locacao(),
                    dias, total, id_locacao,
                ),
            )
            conexao.commit()
            print("\n[+] Locação atualizada com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível atualizar a locação: {erro}")
            return False
        finally:
            cursor.close()

    def remover(self, conexao, id_locacao):
        if not self.locacao_existe(conexao, id_locacao):
            print(f"\n[!] Locação com ID {id_locacao} não encontrada.")
            return False
        confirmacao = input(
            f"Confirma a remoção da locação {id_locacao}? (S/N): "
        ).strip().upper()
        if confirmacao != "S":
            print("\n[-] Operação cancelada.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM locacao WHERE id_locacao = %s", (id_locacao,))
            conexao.commit()
            print("\n[+] Locação removida com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível remover a locação: {erro}")
            return False
        finally:
            cursor.close()
