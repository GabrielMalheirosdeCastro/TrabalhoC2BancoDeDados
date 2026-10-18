class Carro:
    def __init__(self, modelo=None, marca=None, placa=None, valor_diaria=None):
        self.__modelo = modelo
        self.__marca = marca
        self.__placa = placa
        self.__valor_diaria = valor_diaria

    def get_modelo(self): return self.__modelo
    def set_modelo(self, modelo): self.__modelo = modelo

    def get_marca(self): return self.__marca
    def set_marca(self, marca): self.__marca = marca

    def get_placa(self): return self.__placa
    def set_placa(self, placa): self.__placa = placa

    def get_valor_diaria(self): return self.__valor_diaria
    def set_valor_diaria(self, valor_diaria): self.__valor_diaria = valor_diaria

    def __str__(self):
        return (
            f"Placa: {self.__placa} | Modelo: {self.__modelo} | "
            f"Marca: {self.__marca} | Diária: R$ {self.__valor_diaria}"
        )
