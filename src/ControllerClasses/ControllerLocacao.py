class ControllerLocacao:
    def locacao_existe(self, conexao, codigo_locacao):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(1) FROM LOCACOES WHERE CODIGO_LOCACAO = :1",
                (codigo_locacao,),
            )
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close()

    def total_registros(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT COUNT(1) FROM LOCACOES")
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def listar(self, conexao):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                SELECT l.CODIGO_LOCACAO, c.NOME, k.MODELO, l.PLACA,
                       l.DATA_INICIO_LOCACAO, l.DATA_PREVISAO_LOCACAO,
                       l.DATA_FIM_LOCACAO, l.DIAS, l.VALOR_TOTAL
                FROM LOCACOES l
                INNER JOIN CLIENTES c ON l.CPF = c.CPF
                INNER JOIN CARROS k ON l.PLACA = k.PLACA
                ORDER BY l.DATA_INICIO_LOCACAO DESC, l.CODIGO_LOCACAO DESC
                """
            )
            resultados = cursor.fetchall()
        finally:
            cursor.close()

        print("\n--- LISTA DE LOCAÇÕES ---")
        if not resultados:
            print("Nenhuma locação cadastrada.")
        for codigo, nome, modelo, placa, inicio, previsao, fim, dias, total in resultados:
            fim_texto = fim if fim is not None else "Em aberto"
            print(
                f"Código: {codigo} | Cliente: {nome} | Veículo: {modelo} ({placa}) | "
                f"Início: {inicio} | Previsão: {previsao} | Fim: {fim_texto} | "
                f"Dias: {dias} | Total: R$ {float(total):.2f}"
            )
        return resultados

    def inserir(self, conexao, locacao):
        try:
            dias = int(locacao.get_dias())
            total = float(locacao.get_valor_total())
        except (TypeError, ValueError):
            print("\n[!] Dados inválidos para registrar a locação.")
            return False

        cpf = locacao.get_cliente().get_cpf()
        placa = locacao.get_carro().get_placa()
        if dias <= 0 or total < 0:
            print("\n[!] Dias devem ser maiores que zero e o total não pode ser negativo.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO LOCACOES (
                    CODIGO_LOCACAO, DATA_INICIO_LOCACAO, DATA_PREVISAO_LOCACAO,
                    DATA_FIM_LOCACAO, DIAS, VALOR_TOTAL, CPF, PLACA
                )
                VALUES (
                    LOCACOES_CODIGO_LOCACAO_SEQ.NEXTVAL, :1, :2,
                    NULL, :3, :4, :5, :6
                )
                """,
                (
                    locacao.get_data_inicio(), locacao.get_data_previsao(),
                    dias, total, cpf, placa,
                ),
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
        codigo = locacao.get_codigo_locacao()
        if not self.locacao_existe(conexao, codigo):
            print(f"\n[!] Locação de código {codigo} não existe.")
            return False
        try:
            dias = int(locacao.get_dias())
            total = float(locacao.get_valor_total())
        except (TypeError, ValueError):
            print("\n[!] Dados inválidos para atualizar a locação.")
            return False
        if dias <= 0 or total < 0:
            print("\n[!] Dias devem ser maiores que zero e o total não pode ser negativo.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                UPDATE LOCACOES
                SET CPF = :1, PLACA = :2, DATA_INICIO_LOCACAO = :3,
                    DATA_PREVISAO_LOCACAO = :4, DIAS = :5, VALOR_TOTAL = :6
                WHERE CODIGO_LOCACAO = :7
                """,
                (
                    locacao.get_cliente().get_cpf(),
                    locacao.get_carro().get_placa(),
                    locacao.get_data_inicio(),
                    locacao.get_data_previsao(),
                    dias,
                    total,
                    codigo,
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

    def registrar_devolucao(self, conexao, codigo_locacao, data_fim):
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                UPDATE LOCACOES
                SET DATA_FIM_LOCACAO = :1
                WHERE CODIGO_LOCACAO = :2 AND DATA_FIM_LOCACAO IS NULL
                """,
                (data_fim, codigo_locacao),
            )
            if cursor.rowcount == 0:
                conexao.rollback()
                print("\n[!] Locação não encontrada ou já encerrada.")
                return False
            conexao.commit()
            print("\n[+] Devolução registrada com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível registrar a devolução: {erro}")
            return False
        finally:
            cursor.close()

    def remover(self, conexao, codigo_locacao):
        if not self.locacao_existe(conexao, codigo_locacao):
            print(f"\n[!] Locação de código {codigo_locacao} não encontrada.")
            return False
        confirmacao = input(
            f"Confirma a remoção da locação {codigo_locacao}? (S/N): "
        ).strip().upper()
        if confirmacao != "S":
            print("\n[-] Operação cancelada.")
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "DELETE FROM LOCACOES WHERE CODIGO_LOCACAO = :1",
                (codigo_locacao,),
            )
            conexao.commit()
            print("\n[+] Locação removida com sucesso!")
            return True
        except Exception as erro:
            conexao.rollback()
            print(f"\n[!] Não foi possível remover a locação: {erro}")
            return False
        finally:
            cursor.close()
