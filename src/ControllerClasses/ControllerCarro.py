class ControllerCarro:
    def carro_existe(self, conexao, id_carro):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM carro WHERE id_carro = %s", (id_carro,))
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    def total_registros(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM carro")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def listar(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT id_carro, modelo, marca, placa, valor_diaria "
                "FROM carro ORDER BY modelo"
            )
            resultados = cursor.fetchall()
        finally:
            cursor.close()

        print("\n--- LISTA DE CARROS ---")
        if not resultados:
            print("Nenhum carro cadastrado.")
        for row in resultados:
            print(
                f"ID: {row[0]} | Modelo: {row[1]} | Marca: {row[2]} | "
                f"Placa: {row[3]} | Diária: R$ {float(row[4]):.2f}"
            )
        return resultados

    def inserir(self, conexao, carro):
        try:
            diaria = float(carro.get_valor_diaria())
        except (TypeError, ValueError):
            print("\n[!] O valor da diária deve ser numérico.")
            return False

        dados = (
            carro.get_modelo().strip(),
            carro.get_marca().strip(),
            carro.get_placa().strip().upper(),
            diaria,
        )
        if not all(dados[:3]):
            print("\n[!] Modelo, marca e placa são obrigatórios.")
            return False
        if diaria <= 0:
            print("\n[!] O valor da diária deve ser maior que zero.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO carro (modelo, marca, placa, valor_diaria) "
                "VALUES (%s, %s, %s, %s)",
                dados,
            )
            conexao.commit()
            print("\n[+] Carro inserido com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível inserir o carro: {erro}")
            return False
        finally:
            cursor.close()

    def atualizar(self, conexao, carro):
        id_carro = carro.get_id_carro()
        try:
            diaria = float(carro.get_valor_diaria())
        except (TypeError, ValueError):
            print("\n[!] O valor da diária deve ser numérico.")
            return False

        dados = (
            carro.get_modelo().strip(),
            carro.get_marca().strip(),
            carro.get_placa().strip().upper(),
            diaria,
        )
        if not all(dados[:3]) or diaria <= 0:
            print("\n[!] Preencha modelo, marca e placa; a diária deve ser maior que zero.")
            return False
        if not self.carro_existe(conexao, id_carro):
            print(f"\n[!] Carro com ID {id_carro} não existe.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "UPDATE carro SET modelo = %s, marca = %s, placa = %s, "
                "valor_diaria = %s WHERE id_carro = %s",
                (*dados, id_carro),
            )
            conexao.commit()
            print("\n[+] Carro atualizado com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível atualizar o carro: {erro}")
            return False
        finally:
            cursor.close()

    def remover(self, conexao, id_carro):
        if not self.carro_existe(conexao, id_carro):
            print(f"\n[!] Carro com ID {id_carro} não encontrado.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM locacao WHERE id_carro = %s", (id_carro,))
            possui_locacoes = cursor.fetchone()[0] > 0
            if possui_locacoes:
                print(f"\n[!] O carro ID {id_carro} possui locações associadas.")
                confirmacao = input(
                    "Remover o carro e TODAS as locações vinculadas? (S/N): "
                ).strip().upper()
                if confirmacao != "S":
                    conexao.rollback()
                    print("\n[-] Operação cancelada.")
                    return False
                cursor.execute("DELETE FROM locacao WHERE id_carro = %s", (id_carro,))

            cursor.execute("DELETE FROM carro WHERE id_carro = %s", (id_carro,))
            conexao.commit()
            print("\n[+] Carro removido com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível remover o carro: {erro}")
            return False
        finally:
            cursor.close()
