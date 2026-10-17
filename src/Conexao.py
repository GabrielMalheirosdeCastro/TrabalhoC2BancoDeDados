import mysql.connector

class Conexao:
    def __init__(self, host="localhost", database="locadora", user="root", password=""):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return self.conexao
        except Exception as e:
            print(f"\n[Erro] Falha ao conectar ao banco de dados: {e}")
            return None

    def desconectar(self):
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()