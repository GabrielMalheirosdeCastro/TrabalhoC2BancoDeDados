class Carro:
    def __init__(self, id_carro=None, modelo=None, marca=None, placa=None, valor_diaria=None):
        self.__id_carro = id_carro
        self.__modelo = modelo
        self.__marca = marca
        self.__placa = placa
        self.__valor_diaria = valor_diaria

    def get_id_carro(self): return self.__id_carro
    def set_id_carro(self, id_carro): self.__id_carro = id_carro

    def get_modelo(self): return self.__modelo
    def set_modelo(self, modelo): self.__modelo = modelo

    def get_marca(self): return self.__marca
    def set_marca(self, marca): self.__marca = marca

    def get_placa(self): return self.__placa
    def set_placa(self, placa): self.__placa = placa

    def get_valor_diaria(self): return self.__valor_diaria
    def set_valor_diaria(self, valor_diaria): self.__valor_diaria = valor_diaria

    def __str__(self):
        return f"ID: {self.__id_carro} | Modelo: {self.__modelo} | Marca: {self.__marca} | Placa: {self.__placa} | Diária: R$ {self.__valor_diaria}"