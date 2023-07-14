
from abc import ABC, abstractmethod
import random
import Corrida
import json
import time

class Pessoa(ABC):
    "Classe abstrata para definir atributos e métodos comuns aos passageiros e motoristas"

    def __init__(self, nome:str, idade:int, telefone:int, cpf:str) -> None:
        self.set_nome(nome)
        self.set_idade(idade)
        self.set_telefone(telefone)
        self.set_cpf(cpf)

    # Getters
    def get_nome(self) ->str:
        return self.__nome

    def get_idade(self) -> int:
        return self.__idade

    def get_telefone(self) ->int:
        return self.__telefone
    
    def get_cpf(self)->str:
        return self.__cpf
    
    # Setters
    def set_nome(self, nome:str) ->None:
        if not isinstance(nome, str):
            raise ValueError ("\033[31mPor favor, inserir um nome válido\033[m")
        self.__nome = nome

    def set_idade(self, idade:int) ->None:
        if not isinstance(idade, int) or idade < 18:
            raise ValueError ("\033[31mFavor inserir idade maior do que 18 anos\033[m")
        self.__idade = idade
        
    def set_telefone(self, telefone:int) -> None:
        if not isinstance(telefone, int) or len(str(telefone)) != 9:
            raise ValueError ("\033[31mInserir um numero de telefone válido\033[m")
        self.__telefone = telefone

    def set_cpf(self, cpf:str) ->None:
        if not isinstance(cpf, str) or len(str(cpf)) != 11:
            raise ValueError ("\033[31mInserir um CPF válido\033[m")
        self.__cpf = cpf


class Passageiro(Pessoa):
    "Classe para armazenar atributos dos passageiros e ter metodos de informacoes e solicitacao de corrida, método que cria relatorio de corridas e valores pagos"

    def __init__(self, nome: str, idade: int, telefone: int, cpf: str, nota_avaliacao: int = 0) -> None:
        super().__init__(nome, idade, telefone, cpf)
        self.set_nota_avaliacao(nota_avaliacao)

    # Getters
    def get_nota_avaliacao(self) -> int:
        return self.__nota_avaliacao

    # Setters
    def set_nota_avaliacao(self, nota_avaliacao: int) -> None:
        if not isinstance(nota_avaliacao, int) or nota_avaliacao < 1 or nota_avaliacao > 5:
            raise ValueError('\033[31mNota inválida, favor inserir uma nota de 1 a 5\033[m')
        self.__nota_avaliacao = nota_avaliacao


    def iniciar_corrida_passageiro(self, origem: str, destino: str, veiculo:str, categoria: str, forma_pagamento:str) ->None: 
        "Metodo para o passageiro pedir corrida. Instancia um objeto de corrida, em corrida é localizado um motorista conforme critério, que é chamado para responder a resposta retorna em 'chamada'"
        
        iniciar_corrida = Corrida.Corrida() # instancia um objeto para a Classe Corrida (gerenciador)

        valores = iniciar_corrida.valores(categoria, forma_pagamento) #traz os valores da corrida, validação na classe Corrida.
        valor_fim = valores[0] - valores[1] # apura o valor final
        print("\n=========Interface Passageiro===========\n")
        print(f'{((self.get_nome().capitalize()).upper())}, sua corrida terá valor base R$ {valores[0]:.2f} / Veículo Tipo: {veiculo.upper()} / Categoria: {categoria.upper()} / Método Pagamento: {forma_pagamento.upper()} \n\
Desconto pela condição de pagamento: \033[31mR$ -{valores[1]:.2f}\033[m / \033[33mVALOR FINAL: R$ {valor_fim:.2f}\033[m', end='')
        time.sleep(1)

        #pegar a confirmação do Passageiro
        while True:
            aceite = input(str(f' \n    Digite S para aceitar ou N para rejeitar: '))
            aceite = aceite.lower()
            if aceite == 's' or aceite == 'n':
                break
            else:
                print("\033[31mEntrada inválida. Por favor, informe apenas S ou N\033[m")

        if aceite == 's':
            print(f'\nObrigado por aceitar, aguarde que buscaremos por um motorista!')
            time.sleep(1)
        else:
            status = 'cancelado pelo Passageiro'       
            iniciar_corrida.registrar_corrida_passageiro(origem, destino, self._dados_passageiro_corrida(), status, forma_pagamento, self.get_cpf()) #regitrar corrida cancelada pelo passageiro
            return print('\n\033[31mCorrida cancelada! obrigado por escolher nosso aplicativo, chame sempre que precisar!\033[m')

        #Quando um passageiro confirma buscamos por um Motorista e solicitamos confirmação dele
        chamada = iniciar_corrida.iniciar_corrida(origem, destino, veiculo, categoria, self._dados_passageiro_corrida(), forma_pagamento)

        if chamada == 'Não disponível.': #Não temos carros com as caracteristicas solicitadas
            status = 'cancelado indisponibilidade'
            iniciar_corrida.registrar_corrida_passageiro(origem, destino, self._dados_passageiro_corrida(), status, forma_pagamento, self.get_cpf()) #regitrar corrida cancelada por não haver veículo que atenda os requisitos do passageiro
            return print(f'\033[31mInfelizmente não temos veículos que atendam seus requisitos. Por favor, tente novamente em outra categoria\033[m')
        
        elif chamada == 'n': # Motorista recusou a corrida
            status = 'cancelado pelo Motorista'  
            iniciar_corrida.registrar_corrida_passageiro(origem, destino, self._dados_passageiro_corrida(), status, forma_pagamento, self.get_cpf()) #regitrar corrida cancelada pelo Motorista
            print("\n=========Interface Passageiro===========\n")
            print(f'\033[31mInfelizmente não encontramos um motorista disponível para você. Por favor, tente novamente em alguns minutos\033[m')
            return
        
        else: #Veículos e motorista confirmados
            print("\n=========Interface Passageiro===========\n")
            print(f'{((self.get_nome()).capitalize()).upper()} temos uma boa notícia, sua solicitação de corrida foi aceita e quem realizará a corrida será:\n')
            for chave, valor in chamada[1].items():
                if isinstance(valor, dict):
                    print(f"Dados do {chave.capitalize()}:") 
                    for subchave, subvalor in valor.items():
                        print(f"{subchave.capitalize()}: {subvalor}")  
                else:
                    print(f"{chave.capitalize()}: {valor}")
            
            status = 'realizada'
            iniciar_corrida.registrar_corrida_passageiro(origem, destino, self._dados_passageiro_corrida(), status, forma_pagamento, self.get_cpf(), chamada[1]) #regitrar corrida efetivada
            
    def _dados_passageiro_corrida(self):
        "metodo que devolve dicionário com dados do passageiro"
        return {'Nome Passageiro': self.get_nome(),
                'Telefone': self.get_telefone(),
                'Avaliacao': self.get_nota_avaliacao(),
                }
    
    def relatorio_passageiro(self,cpf:str) ->str:
        "Método que devolve o relatorio das corridas realizadas do passageiro com base no CPF informado"
        if not isinstance(cpf, str) or len(str(cpf)) != 11:
            raise ValueError ("\033[31mInserir um CPF válido\033[m")
        consultar = Corrida.Corrida()
        relatorio = consultar.consulta_corridas_passageiros(cpf)
        return (relatorio)

class Motorista_Corrida(Pessoa):
    "Classe motorista para processar solicitações de corridas para o Motoristas "

    def __init__(self, nome: str, idade: int, telefone: int, cpf: int, carro: dict, cnh: str, nota_avaliacao: int=0) -> None:
        super().__init__(nome, idade, telefone, cpf)
        self.carro = carro #a validação ocorreu na classe veículo
        self.set_nota_avaliacao(nota_avaliacao)
        self.set_cnh(cnh)

    def aceitar_corrida(self, dados_chamada:str, key_motorista:str) ->str:
        "Metodo para aceitar ou rejeitar a corrida pelo Motorista"

        print("\n=========Interface Motorista===========\n")
        print(f'Motorista: {((self.get_nome()).capitalize()).upper()}, registro nº {key_motorista}\n {dados_chamada}\n')
        time.sleep(1)
        while True:
            resposta = input(str('  Digite S para aceitar ou N para rejeitar: '))
            resposta = resposta.lower()
            if resposta == 's' or resposta =='n':
                break
            else:
                print("\033[31mEntrada inválida. Por favor, informe apenas S ou N\033[m")
        if resposta == 's':
            return [resposta, self._dados_motorista_corrida()]
        else:
            return resposta
        
    def _dados_motorista_corrida(self) -> dict:
     "Relatório com todos os dados gerais para usar no relatório de corridas"
     carro = self.get_carro()
     return {'Motorista': self.get_nome(),
        'Telefone': self.get_telefone(),
        'Avaliação': self.__nota_avaliacao,
        'Veículo': {'tipo': carro['Tipo'], 'marca': carro['marca'], 'ano': carro['ano']},
        }

    # Getters: retorno de informação
    def get_nota_avaliacao(self) -> int:
        return self.__nota_avaliacao
    
    def get_cnh(self) ->str:
        return self.__cnh
    
    def get_carro(self) ->dict:
        return self.carro

    # Setters: conforme peculiaridade de cada atributo, fazem a validação e gravam os valores nas variáveis
    def set_nota_avaliacao(self, nota_avaliacao:int) -> None:
        if not isinstance(nota_avaliacao, int) or nota_avaliacao <1 or nota_avaliacao > 5:
            raise ValueError ('\033[31mNota inválida, favor inserir uma nota de 1 a 5\033[m')
        self.__nota_avaliacao = nota_avaliacao

    def set_cnh(self, cnh:str) ->None:
        if not isinstance(cnh, str) or len(str(cnh)) != 11:
            raise ValueError ("\033[31mInserir um numero de CNH válido\033[m")
        self.__cnh = cnh


class Motorista_Cadastro(Pessoa):
    "Classe para cadastrar e armazenar dados dos motoristas em banco de dados Json"

    def __init__(self, nome: str, idade: int, telefone: int, cpf: str, carro: dict, cnh: str, nota_avaliacao: int=0) -> None:
        # Carregar dados do arquivo JSON
        try:
            with open('registro_motoristas.json', 'r') as arquivo_json:
                self.registro_motoristas = json.load(arquivo_json)
        except FileNotFoundError:
            self.registro_motoristas = {}

        # Verificar se o motorista já existe
        for key, value in self.registro_motoristas.items():
            if value.get('cpf') == cpf:
                raise ValueError('\033[31mMotorista já cadastrado\033[m')

        super().__init__(nome, idade, telefone, cpf)
        self.carro = carro
        self.set_nota_avaliacao(nota_avaliacao)
        self.set_cnh(cnh)
        self.id_motorista = random.randint(1, 1000)

        self.registro_motoristas[self.id_motorista] = {'Motorista': self.get_nome(),
                                                       'Idade': self.get_idade(),
                                                       'Telefone': self.get_telefone(),
                                                       'cpf': self.get_cpf(),
                                                       'CNH': self.get_cnh(),
                                                       'Veiculo': self.carro,
                                                       'Avaliacao': self.__nota_avaliacao,
                                                       }
        
        with open('registro_motoristas.json', 'w') as arquivo_json:
            json.dump(self.registro_motoristas, arquivo_json)

    # Getters:
    def get_nota_avaliacao(self) -> int:
        return self.__nota_avaliacao
    
    def get_cnh(self) ->str:
        return self.__cnh
    
    # Setters: 
    def set_nota_avaliacao(self, nota_avaliacao:int) -> None:
        if not isinstance(nota_avaliacao, int) or nota_avaliacao <1 or nota_avaliacao > 5:
            raise ValueError ('\033[31mNota inválida, favor inserir uma nota de 1 a 5\033[m')
        self.__nota_avaliacao = nota_avaliacao

    def set_cnh(self, cnh:str) ->None:
        if not isinstance(cnh, str) or len(str(cnh)) != 11:
            raise ValueError ("\033[31mInserir um numero de CNH válido\033[m")
        self.__cnh = cnh


