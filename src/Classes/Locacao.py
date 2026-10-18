class Locacao:
    def __init__(
        self,
        codigo_locacao=None,
        cliente=None,
        carro=None,
        data_inicio=None,
        data_previsao=None,
        data_fim=None,
        dias=None,
        valor_total=None,
    ):
        self.__codigo_locacao = codigo_locacao
        self.__cliente = cliente
        self.__carro = carro
        self.__data_inicio = data_inicio
        self.__data_previsao = data_previsao
        self.__data_fim = data_fim
        self.__dias = dias
        self.__valor_total = valor_total

    def get_codigo_locacao(self): return self.__codigo_locacao
    def set_codigo_locacao(self, codigo_locacao): self.__codigo_locacao = codigo_locacao

    def get_cliente(self): return self.__cliente
    def set_cliente(self, cliente): self.__cliente = cliente

    def get_carro(self): return self.__carro
    def set_carro(self, carro): self.__carro = carro

    def get_data_inicio(self): return self.__data_inicio
    def set_data_inicio(self, data_inicio): self.__data_inicio = data_inicio

    def get_data_previsao(self): return self.__data_previsao
    def set_data_previsao(self, data_previsao): self.__data_previsao = data_previsao

    def get_data_fim(self): return self.__data_fim
    def set_data_fim(self, data_fim): self.__data_fim = data_fim

    def get_dias(self): return self.__dias
    def set_dias(self, dias): self.__dias = dias

    def get_valor_total(self): return self.__valor_total
    def set_valor_total(self, valor_total): self.__valor_total = valor_total
