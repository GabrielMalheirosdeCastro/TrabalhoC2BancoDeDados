class ControllerCarro:
    def __init__(self):
        pass

    def carro_existe(self, conexao, id_carro):
        """Verifica se um carro existe pelo ID"""
        cursor = conexao.cursor()
        sql = "SELECT COUNT(1) FROM carro WHERE id_carro = " + str(id_carro)
        cursor.execute(sql)
        existe = cursor.fetchone()[0] > 0
        cursor.close()
        return existe

    def total_registros(self, conexao):
        """Contagem para Splash Screen"""
        cursor = conexao.cursor()
        sql = "SELECT COUNT(1) total_carro FROM carro"
        cursor.execute(sql)
        total = cursor.fetchone()[0]
        cursor.close()
        return total

    def listar(self, conexao):
        """Lista todas as tuplas com PK e campo descritivo (Item 6.c.3 / 6.d.3)"""
        cursor = conexao.cursor()
        sql = "SELECT id_carro, modelo, marca, placa, valor_diaria FROM carro"
        cursor.execute(sql)
        resultados = cursor.fetchall()
        cursor.close()

        print("\n--- LISTA DE CARROS ---")
        for row in resultados:
            print(f"ID: {row[0]} | Modelo: {row[1]} | Marca: {row[2]} | Placa: {row[3]} | Diária: R$ {row[4]}")
        return resultados

    def inserir(self, conexao, carro):
        """Inserção de novo carro (Item 6.b)"""
        cursor = conexao.cursor()
        sql = "INSERT INTO carro (modelo, marca, placa, valor_diaria) VALUES ('" + carro.get_modelo() + "', '" + carro.get_marca() + "', '" + carro.get_placa() + "', " + str(carro.get_valor_diaria()) + ")"
        cursor.execute(sql)
        conexao.commit()
        cursor.close()
        print("\n[+] Carro inserido com sucesso!")

    def atualizar(self, conexao, carro):
        """Atualização de carro existente (Item 6.d)"""
        if not self.carro_existe(conexao, carro.get_id_carro()):
            print(f"\n[!] Erro: Carro com ID {carro.get_id_carro()} não existe.")
            return

        cursor = conexao.cursor()
        sql = "UPDATE carro SET modelo = '" + carro.get_modelo() + "', marca = '" + carro.get_marca() + "', placa = '" + carro.get_placa() + "', valor_diaria = " + str(carro.get_valor_diaria()) + " WHERE id_carro = " + str(carro.get_id_carro())
        cursor.execute(sql)
        conexao.commit()
        cursor.close()
        print("\n[+] Carro atualizado com sucesso!")

    def remover(self, conexao, id_carro):
        """Remoção de carro com tratamento de FK (Item 6.c)"""
        if not self.carro_existe(conexao, id_carro):
            print(f"\n[!] Erro: Carro com ID {id_carro} não encontrado.")
            return

        cursor = conexao.cursor()

        # Verificação de Foreign Key em locacao (Item 6.c.5.i)
        sql_fk = "SELECT COUNT(1) FROM locacao WHERE id_carro = " + str(id_carro)
        cursor.execute(sql_fk)
        has_fk = cursor.fetchone()[0]

        if has_fk > 0:
            print(f"\n[!] Atenção: O carro ID {id_carro} possui locações associadas!")
            confirmacao = input("Deseja remover o carro E TODAS as locações vinculadas a ele? (S/N): ")
            if confirmacao.upper() == 'S':
                sql_del_filha = "DELETE FROM locacao WHERE id_carro = " + str(id_carro)
                cursor.execute(sql_del_filha)
            else:
                print("\n[-] Operação cancelada.")
                cursor.close()
                return

        sql_del_pai = "DELETE FROM carro WHERE id_carro = " + str(id_carro)
        cursor.execute(sql_del_pai)
        conexao.commit()
        cursor.close()
        print("\n[+] Carro removido com sucesso!")