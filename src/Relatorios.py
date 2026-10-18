class Relatorios:
    def __init__(self, conexao):
        self.conexao = conexao

    def relatorio_locacoes_detalhadas(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """
                SELECT l.id_locacao, c.nome, k.modelo, k.placa,
                       l.data_locacao, l.dias, l.valor_total
                FROM locacao l
                INNER JOIN cliente c ON l.id_cliente = c.id_cliente
                INNER JOIN carro k ON l.id_carro = k.id_carro
                ORDER BY l.data_locacao DESC, l.id_locacao DESC
                """
            )
            resultados = cursor.fetchall()
        finally:
            cursor.close()

        print("\n--- RELATÓRIO DE LOCAÇÕES DETALHADAS ---")
        if not resultados:
            print("Ainda não há locações para exibir.")
            return
        for row in resultados:
            print(
                f"Locação #{row[0]} | Cliente: {row[1]} | "
                f"Veículo: {row[2]} ({row[3]}) | Data: {row[4]} | "
                f"Dias: {row[5]} | Total: R$ {float(row[6]):.2f}"
            )

    def relatorio_faturamento_por_modelo(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute(
                """
                SELECT k.modelo, COUNT(l.id_locacao) AS qtd_locacoes,
                       COALESCE(SUM(l.valor_total), 0) AS total_faturado
                FROM carro k
                LEFT JOIN locacao l ON l.id_carro = k.id_carro
                GROUP BY k.id_carro, k.modelo
                ORDER BY total_faturado DESC, k.modelo
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
