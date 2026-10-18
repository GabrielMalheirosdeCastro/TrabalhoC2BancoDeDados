from pathlib import Path

import oracledb


class Conexao:
    def __init__(self, host="localhost", porta=1521, servico="XEPDB1"):
        self.dsn = f"{host}:{porta}/{servico}"
        credentials_path = (
            Path(__file__).resolve().parent
            / "conexion"
            / "passphrase"
            / "authentication.oracle"
        )
        credentials = credentials_path.read_text(encoding="utf-8").strip().split(",", maxsplit=1)
        if len(credentials) != 2 or not all(value.strip() for value in credentials):
            raise ValueError(
                f"Credenciais Oracle inválidas em {credentials_path}; "
                "use o formato usuario,senha."
            )
        self.user, self.password = (value.strip() for value in credentials)
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
