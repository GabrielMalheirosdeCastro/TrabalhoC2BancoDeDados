class ControllerCarro:
    def carro_existe(self, conexao, placa):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM CARROS WHERE PLACA = :1", (placa,))
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    def total_registros(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM CARROS")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def listar(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT PLACA, MODELO, MARCA, VALOR_DIARIA "
                "FROM CARROS ORDER BY MODELO"
            )
            resultados = cursor.fetchall()
        finally:
            cursor.close()

        print("\n--- LISTA DE CARROS ---")
        if not resultados:
            print("Nenhum carro cadastrado.")
        for placa, modelo, marca, diaria in resultados:
            print(
                f"Placa: {placa} | Modelo: {modelo} | Marca: {marca} | "
                f"Diária: R$ {float(diaria):.2f}"
            )
        return resultados

    def inserir(self, conexao, carro):
        try:
            diaria = float(carro.get_valor_diaria())
        except (TypeError, ValueError):
            print("\n[!] O valor da diária deve ser numérico.")
            return False

        placa = carro.get_placa().strip().upper()
        dados = (placa, carro.get_modelo().strip(), carro.get_marca().strip(), diaria)
        if not all(dados[:3]):
            print("\n[!] Placa, modelo e marca são obrigatórios.")
            return False
        if len(placa) > 7:
            print("\n[!] A placa pode ter no máximo 7 caracteres.")
            return False
        if diaria <= 0:
            print("\n[!] O valor da diária deve ser maior que zero.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO CARROS (PLACA, MODELO, MARCA, VALOR_DIARIA) "
                "VALUES (:1, :2, :3, :4)",
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

    def atualizar(self, conexao, placa_atual, carro):
        placa_nova = carro.get_placa().strip().upper()
        try:
            diaria = float(carro.get_valor_diaria())
        except (TypeError, ValueError):
            print("\n[!] O valor da diária deve ser numérico.")
            return False

        modelo = carro.get_modelo().strip()
        marca = carro.get_marca().strip()
        if not modelo or not marca or not placa_nova or diaria <= 0:
            print("\n[!] Preencha placa, modelo e marca; a diária deve ser maior que zero.")
            return False
        if len(placa_nova) > 7:
            print("\n[!] A placa pode ter no máximo 7 caracteres.")
            return False
        if not self.carro_existe(conexao, placa_atual):
            print(f"\n[!] Carro com placa {placa_atual} não existe.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(1) FROM LOCACOES WHERE PLACA = :1",
                (placa_atual,),
            )
            possui_locacoes = cursor.fetchone()[0] > 0
            if possui_locacoes and placa_nova != placa_atual:
                print("\n[!] Não é possível alterar a placa de um carro com locações.")
                return False
            cursor.execute(
                "UPDATE CARROS SET PLACA = :1, MODELO = :2, MARCA = :3, "
                "VALOR_DIARIA = :4 WHERE PLACA = :5",
                (placa_nova, modelo, marca, diaria, placa_atual),
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

    def remover(self, conexao, placa):
        if not self.carro_existe(conexao, placa):
            print(f"\n[!] Carro com placa {placa} não encontrado.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM LOCACOES WHERE PLACA = :1", (placa,))
            possui_locacoes = cursor.fetchone()[0] > 0
            if possui_locacoes:
                print(f"\n[!] O carro de placa {placa} possui locações associadas.")
                confirmacao = input(
                    "Remover o carro e TODAS as locações vinculadas? (S/N): "
                ).strip().upper()
                if confirmacao != "S":
                    conexao.rollback()
                    print("\n[-] Operação cancelada.")
                    return False
                cursor.execute("DELETE FROM LOCACOES WHERE PLACA = :1", (placa,))

            cursor.execute("DELETE FROM CARROS WHERE PLACA = :1", (placa,))
            conexao.commit()
            print("\n[+] Carro removido com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível remover o carro: {erro}")
            return False
        finally:
            cursor.close()
