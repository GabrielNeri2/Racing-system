from abc import ABC, abstractmethod
import datetime


class Veiculo(ABC):
    "Classe abstrata que define a construção das Classes Carro e Moto"
    def __init__(self, placa:str, modelo:str, marca:str, ano:int, cor:str) -> None:

        self.set_placa(placa)
        self.set_modelo(modelo)
        self.set_marca(marca)
        self.set_ano(ano)
        self.set_cor(cor)

    # Getters: retorno de informações
    def get_marca(self):
        return self.__marca

    def get_modelo(self):
        return self.__modelo

    def get_ano(self):
        return self.__ano

    def get_cor(self):
        return self.__cor

    def get_placa(self):
        return self.__placa

    # Setters: conforme peculiaridade de cada atributo, fazem a validação e gravam os valores nas variáveis
    def set_placa(self, placa):
        if not isinstance(placa, str) or len(placa) != 7:
            raise ValueError("\033[31mPlaca deve ser uma string de 7 caracteres\033[m")
        placa =  placa.upper()
        self.__placa = placa

    def set_modelo(self, modelo):
        if not isinstance(modelo, str):
            raise ValueError("\033[31mModelo deve ser uma string\033[m")
        modelo = modelo.lower()
        self.__modelo = modelo

    def set_marca(self, marca):
        if not isinstance(marca, str):
            raise ValueError("\033[31mMarca deve ser uma string\033[m")
        marca = marca.lower()
        self.__marca = marca

    def set_ano(self, ano):
        limite = datetime.date.today().year - 10
        if not isinstance(ano, int) or ano < limite or ano > 2023:
            raise ValueError(f"\033[31mAno deve ser um inteiro não menor que {limite} e o ano atual\033[m")
        self.__ano = ano

    def set_cor(self, cor):
        if not isinstance(cor, str):
            raise ValueError("\033[31mCor deve ser uma string\033[m")
        cor = cor.lower()
        self.__cor = cor

class Carro(Veiculo):
    "Classe concreta para reunir dados sobre os carros"
    def __init__(self, placa:str, modelo:str, marca:str, ano:int, cor:str, n_de_portas:int, numero_de_lugares:int) -> None:
        super().__init__(placa, modelo, marca, ano, cor)
        self.set_n_de_portas(n_de_portas)
        self.set_numero_de_lugares(numero_de_lugares)
        self.__tipo = 'carro'

    # Setters: conforme peculiaridade de cada atributo, fazem a validação e gravam os valores nas variáveis
    def set_n_de_portas(self, n_de_portas) -> None:
        if not isinstance(n_de_portas, int) or n_de_portas <= 2:
            raise ValueError("\033[31mNúmero de portas deve ser um inteiro maior do que 2\033[m")
        self.__n_de_portas = n_de_portas

    def set_numero_de_lugares(self, numero_de_lugares)-> None:
        if not isinstance(numero_de_lugares, int) or numero_de_lugares <= 0:
            raise ValueError("\033[31mNúmero de lugares deve ser um inteiro positivo\033[m")
        self.__numero_de_lugares = numero_de_lugares

    # Método para retornar todos os atributos como um dicionário
    def get_atributos(self) -> dict:
        return {'Tipo': self.__tipo,
                "placa": self.get_placa(),
                "modelo": self.get_modelo(),
                "marca": self.get_marca(),
                "ano": self.get_ano(),
                "cor": self.get_cor(),
                "n_de_portas": self.__n_de_portas,
                "numero_de_lugares": self.__numero_de_lugares,
                }

class Moto(Veiculo):
    "Classe concreta para reunir dados sobre os carros"
    def __init__(self, placa:str, modelo:str, marca:str, ano:int, cor:str, cilindradas:int) -> None:
        super().__init__(placa, modelo, marca, ano, cor)
        self.set_cilindradas(cilindradas)
        self.__tipo = 'moto'

    # Getter: retorno de informações
    def get_cilindradas(self):
        return self.__cilindradas

    # Setter: conforme peculiaridade do atributo, realizar a validação e gravar os valores na variável
    def set_cilindradas(self, cilindradas):
        if not isinstance(cilindradas, int) or cilindradas <= 0:
            raise ValueError("\033[31mCilindradas deve ser um inteiro positivo\033[m")
        self.__cilindradas = cilindradas

    # Método para retornar todos os atributos como um dicionário
    def get_atributos(self) ->dict:
        return {'Tipo': self.__tipo,
            "placa": self.get_placa(),
            "modelo": self.get_modelo(),
            "marca": self.get_marca(),
            "ano": self.get_ano(),
            "cor": self.get_cor(),
            "cilindradas": self.__cilindradas,
        }
