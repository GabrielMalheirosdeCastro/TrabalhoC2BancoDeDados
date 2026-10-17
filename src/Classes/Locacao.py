class Locacao:
    def __init__(self, id_locacao=None, cliente=None, carro=None, data_locacao=None, dias=None, valor_total=None):
        self.__id_locacao = id_locacao
        self.__cliente = cliente  # Instância de Cliente
        self.__carro = carro      # Instância de Carro
        self.__data_locacao = data_locacao
        self.__dias = dias
        self.__valor_total = valor_total

    def get_id_locacao(self): return self.__id_locacao
    def set_id_locacao(self, id_locacao): self.__id_locacao = id_locacao

    def get_cliente(self): return self.__cliente
    def set_cliente(self, cliente): self.__cliente = cliente

    def get_carro(self): return self.__carro
    def set_carro(self, carro): self.__carro = carro

    def get_data_locacao(self): return self.__data_locacao
    def set_data_locacao(self, data_locacao): self.__data_locacao = data_locacao

    def get_dias(self): return self.__dias
    def set_dias(self, dias): self.__dias = dias

    def get_valor_total(self): return self.__valor_total
    def set_valor_total(self, valor_total): self.__valor_total = valor_total

    def __str__(self):
        return f"Locação #{self.__id_locacao} | Cliente: {self.__cliente.get_nome()} | Carro: {self.__carro.get_modelo()} | Dias: {self.__dias} | Total: R$ {self.__valor_total}"