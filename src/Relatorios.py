class Relatorios:
    def __init__(self, conexao):
        self.conexao = conexao

    def relatorio_locacoes_detalhadas(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """
                SELECT l.CODIGO_LOCACAO, c.NOME, k.MODELO, k.PLACA,
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

        print("\n--- RELATÓRIO DE LOCAÇÕES DETALHADAS ---")
        if not resultados:
            print("Ainda não há locações para exibir.")
            return
        for codigo, nome, modelo, placa, inicio, previsao, fim, dias, total in resultados:
            fim_texto = fim if fim is not None else "Em aberto"
            print(
                f"Locação #{codigo} | Cliente: {nome} | "
                f"Veículo: {modelo} ({placa}) | Início: {inicio} | "
                f"Previsão: {previsao} | Fim: {fim_texto} | "
                f"Dias: {dias} | Total: R$ {float(total):.2f}"
            )

    def relatorio_faturamento_por_modelo(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """
                SELECT k.MODELO, COUNT(l.CODIGO_LOCACAO) AS QTD_LOCACOES,
                       COALESCE(SUM(l.VALOR_TOTAL), 0) AS TOTAL_FATURADO
                FROM CARROS k
                LEFT JOIN LOCACOES l ON l.PLACA = k.PLACA
                GROUP BY k.PLACA, k.MODELO
                ORDER BY TOTAL_FATURADO DESC, k.MODELO
                """
            )
            resultados = cursor.fetchall()
        finally:
            cursor.close()

        print("\n--- FATURAMENTO POR MODELO DE CARRO ---")
        if not resultados:
            print("Nenhum carro cadastrado para gerar o relatório.")
            return
        for modelo, quantidade, faturamento in resultados:
            print(
                f"Modelo: {modelo} | Locações: {quantidade} | "
                f"Faturamento: R$ {float(faturamento):.2f}"
            )
