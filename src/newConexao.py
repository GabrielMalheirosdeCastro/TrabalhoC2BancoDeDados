import oracledb

class Conexao:
    def __init__(self, host="localhost", porta=1521, servico="XEPDB1",
                 user="locadora", password=""):
        self.dsn = f"{host}:{porta}/{servico}"
        self.user = user
        self.password = password
        self.conexao = None

    def conectar(self):
        try:
            self.conexao = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn
            )
            return self.conexao
        except oracledb.Error as e:
            print(f"\n[Erro] Falha ao conectar ao banco de dados: {e}")
            return None

    def desconectar(self):
        if self.conexao:
            try:
                self.conexao.close()
            except oracledb.Error:
                pass
            finally:
                self.conexao = None
