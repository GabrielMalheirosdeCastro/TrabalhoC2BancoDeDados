class Relatorios:
    def __init__(self, conexao):
        self.conexao = conexao

    def relatorio_locacoes_detalhadas(self):
        """ Relatório 1 (JOIN): Lista as locações detalhando cliente e veículo """
        cursor = self.conexao.cursor()
        sql = """
            SELECT l.id_locacao, c.nome, k.modelo, k.placa, l.dias, l.valor_total
            FROM locacao l
            INNER JOIN cliente c ON l.id_cliente = c.id_cliente
            INNER JOIN carro k ON l.id_carro = k.id_carro
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()

        print("\n--- RELATÓRIO DE LOCAÇÕES DETALHADAS (JOIN) ---")
        for row in resultados:
            print(f"ID Locação: {row[0]} | Cliente: {row[1]} | Carro: {row[2]} ({row[3]}) | Dias: {row[4]} | Total: R$ {row[5]}")

    def relatorio_faturamento_por_modelo(self):
        """ Relatório 2 (GROUP BY / SUMARIZAÇÃO): Agrupa total arrecadado e locações por modelo """
        cursor = self.conexao.cursor()
        sql = """
            SELECT k.modelo, COUNT(l.id_locacao) AS qtd_locacoes, SUM(l.valor_total) AS total_faturado
            FROM locacao l
            INNER JOIN carro k ON l.id_carro = k.id_carro
            GROUP BY k.modelo
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()

        print("\n--- RELATÓRIO DE FATURAMENTO POR MODELO DE CARRO (GROUP BY) ---")
        for row in resultados:
            print(f"Modelo: {row[0]} | Qtd. Locações: {row[1]} | Faturamento Total: R$ {row[2]}")