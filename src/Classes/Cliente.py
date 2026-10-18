class Cliente:
    def __init__(self, cpf=None, nome=None, telefone=None):
        self.__cpf = cpf
        self.__nome = nome
        self.__telefone = telefone

    def get_cpf(self): return self.__cpf
    def set_cpf(self, cpf): self.__cpf = cpf

    def get_nome(self): return self.__nome
    def set_nome(self, nome): self.__nome = nome

    def get_telefone(self): return self.__telefone
    def set_telefone(self, telefone): self.__telefone = telefone

    def __str__(self):
        return f"CPF: {self.__cpf} | Nome: {self.__nome} | Tel: {self.__telefone}"
