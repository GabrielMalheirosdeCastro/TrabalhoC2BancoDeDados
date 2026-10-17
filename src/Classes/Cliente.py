class Cliente:
    def __init__(self, id_cliente=None, nome=None, cpf=None, telefone=None):
        self.__id_cliente = id_cliente
        self.__nome = nome
        self.__cpf = cpf
        self.__telefone = telefone

    def get_id_cliente(self): return self.__id_cliente
    def set_id_cliente(self, id_cliente): self.__id_cliente = id_cliente

    def get_nome(self): return self.__nome
    def set_nome(self, nome): self.__nome = nome

    def get_cpf(self): return self.__cpf
    def set_cpf(self, cpf): self.__cpf = cpf

    def get_telefone(self): return self.__telefone
    def set_telefone(self, telefone): self.__telefone = telefone

    def __str__(self):
        return f"ID: {self.__id_cliente} | Nome: {self.__nome} | CPF: {self.__cpf} | Tel: {self.__telefone}"