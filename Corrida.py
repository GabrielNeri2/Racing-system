from random import randint
import Pessoas
import Pagamento
import json
import random

class Corrida():
    "Classe que armazena dados_passageiro das corridas e processa informações entre as classes envolvidas"

    __corridas_motoristas = {} # dict atributo para armazenar os dados_passageiro das corridas para motoristas
    __corridas_passageiros = {} # dict atributo para armazenar os dados_passageiro das corridas para passageiros

    @classmethod
    def adicionar_corrida_motorista(cls, id_corrida, dados_corrida):
        cls.__corridas_motoristas[id_corrida] = dados_corrida
    @classmethod
    def adicionar_corrida_passageiro(cls, id_corrida, dados_corrida):
        cls.__corridas_passageiros[id_corrida] = dados_corrida
    @classmethod
    def get_corridas_motoristas(cls):
        return cls.__corridas_motoristas
    @classmethod
    def get_corridas_passageiros(cls):
        return cls.__corridas_passageiros

    def __init__(self) -> None:
        self.__distancia = randint(5, 20)  # Distância gerada aleatoriamente para o exemplo
        self.__tempo = randint(10, 30)  # Tempo gerado aleatoriamente para o exemplo
        self.__valorfinal = None #cria atributo para o valor da corrida
        self.__valordesconto = None #cria atributo para o desconto
        self.__id_corrida = randint(100, 1000000)


    def iniciar_corrida(self, origem: str, destino: str, veiculo:str, categoria: str, dados_passageiro: dict, forma_pagamento:str):
        "Metodo para o Passageiro iniciar uma corrida e chamar o aceite do Motorista"

        # validar os parametros origem, destino, veiculo e categoria, demais já validados_passageiro
        self._validar_dados_passageiro(origem=origem, destino=destino, veiculo=veiculo, categoria=categoria) #validação dos parametros não validados_passageiro anteriormente
            
        # localizar um motorista que atenda os requisitos da viagem:
        motorista = self._localizar_motorista(categoria, veiculo)
    
        if motorista == 'Não disponível':
            return motorista
            
        # Acessar as informações do motorista:
        info = list(motorista.values())[0]
        chave_motorista = list(motorista.keys())[0]

        # Criar um objeto 'motorista' da classe Motorista_Corrida
        motorista_chamado = Pessoas.Motorista_Corrida(
            nome=info.get('Motorista'),
            idade=info.get('Idade'),
            telefone=info.get('Telefone'),
            cpf=info.get('cpf'),
            carro=info.get('Veiculo'),
            cnh=info.get('CNH'),
            nota_avaliacao=info.get('Avaliacao')
        )
        # Chamar a resposta do Motorista s/n:
        dados_passageiro_chamada = (f" \nSOLICITAÇÃO DE CORRIDA \nPassageiro: {((dados_passageiro['Nome Passageiro']).capitalize().upper())} / Telefone: {dados_passageiro['Telefone']} / Nota Avaliação: {dados_passageiro['Avaliacao']}\n\
ORIGEM: {(origem.capitalize())} / DESTINO: {(destino.capitalize())} / DISTÂNCIA: {self.__distancia} KM / TEMPO: {self.__tempo} MIN\nCategoria: {((categoria).capitalize()).upper()} / Método Pagamento: {((forma_pagamento).capitalize()).upper()} \n\
Valor Base: R$ {self.__valorfinal:.2f} / \033[31mDesconto R$ -{self.__valordesconto:.2f}\033[m \n\
\033[33mVALOR FINAL: R$ {(self.__valorfinal - self.__valordesconto):.2f}\033[m")
        
        consulta = motorista_chamado.aceitar_corrida(dados_passageiro_chamada, chave_motorista)
        
        if consulta == 'n':
            status = 'cancelado pelo Motorista'
            self.registrar_corrida_motorista(origem, destino,dados_passageiro, status, motorista, forma_pagamento)
            return consulta
        
        else:
            status = 'realizada'
            self.registrar_corrida_motorista(origem, destino,dados_passageiro, status, motorista, forma_pagamento)
            return consulta
    
    def valores(self, categoria:str, forma_pagamento:str) ->list:
        "Processar o valor da Corrida"

        # Validar categoria e forma_pagamento
        self._validar_dados_passageiro(categoria=categoria, forma_pagamento=forma_pagamento)

        # Instanciar a classe Pagamento e chamar método para apurar o valor base e o valor do desconto
        valores = Pagamento.Pagamento()

        valores = valores.valores_corrida(self.__distancia, self.__tempo, categoria, forma_pagamento)

        self.__valorfinal = valores[0] #valor sem desconto
        self.__valordesconto = valores[1] #valor do desconto

        return valores


    def _localizar_motorista(self, categoria:str, veiculo:str) ->dict:
        "Método interno para buscar um motorista que atenda os requisitos do chamado"

        # Abrir o arquivo JSON e carregar o dicionário
        with open('registro_motoristas.json', 'r') as f:
            data = json.load(f)

        # Criar uma lista para armazenar os motoristas que satisfazem as condições
        motoristas_validos = []

        if categoria == 'luxo':
            for key, value in data.items():
                veiculo_info = value.get('Veiculo')
                avaliacao = value.get('Avaliacao')
                if (veiculo_info.get('Tipo') == veiculo and avaliacao is not None and 
                    veiculo_info.get('n_de_portas') == 5 and
                    veiculo_info.get('numero_de_lugares') == 5 and 
                    avaliacao >= 4 and veiculo_info.get('ano') >= 2018):
                        motoristas_validos.append({key: value}) # adicionar o motorista à lista

            if not motoristas_validos:
                return 'Não disponível' #se a lista está vazia o retorno é uma string

        else:
            for key, value in data.items():
                veiculo_info = value.get('Veiculo')
                avaliacao = value.get('Avaliacao')
                if (veiculo_info is not None and avaliacao is not None and
                        veiculo_info.get('Tipo') == veiculo):
                    motoristas_validos.append({key: value})  # adicionar o motorista à lista

            # Se a lista estiver vazia, significa que nenhum motorista atendeu às condições
            if not motoristas_validos:
                return 'Não disponível' #se a lista está vazia o retorno é uma string

        # Escolher um motorista aleatoriamente da lista de motoristas válidos
        motorista_escolhido = random.choice(motoristas_validos)
        
        return (motorista_escolhido) # retorna um dicionário pois os itens da lista são dicionários.


    def registrar_corrida_passageiro(self, origem:str, destino:str, dados_passageiro:dict,status:str, forma_pagamento:str, cpf:str, motorista:dict = None) -> None:
        # Método para registar corridas do Passageiro
        if motorista is None:
            motorista = {}

        veiculo = motorista.get('Veículo', {})
        corrida = {
            'Passageiro': dados_passageiro.get('Nome Passageiro', None),
            'CPF': cpf,
            'Telefone': dados_passageiro.get('Telefone', None),
            'Motorista': motorista.get('Motorista', None),
            'Telefone Motorista': motorista.get('Telefone', None),
            'Avaliação Motorista': motorista.get('Avaliação', None),
            'Veículo': {
                'tipo': veiculo.get('tipo', None),
                'marca': veiculo.get('marca', None),
                'ano': veiculo.get('ano', None),
            },
            'origem': origem, 
            'destino': destino,
            'distancia': self.__distancia,
            'tempo corrida': self.__tempo,
            'valor base': round(self.__valorfinal,2),
            'desconto': round(self.__valordesconto,2),
            'valor final':round((self.__valorfinal - self.__valordesconto),2),
            'Forma Pagamento' : forma_pagamento,
            'status': status
        }
        Corrida.adicionar_corrida_passageiro(self.__id_corrida, corrida)
        return 
    

    def registrar_corrida_motorista(self, origem:str, destino:str, dados_passageiro:dict, status:str, motorista:dict, forma_pagamento:str) -> None:
        # Método para registar corridas do Motorista

        motorista_id, motorista_info = list(motorista.items())[0]  # Pega o ID e as informações do motorista
        veiculo = motorista_info.get('Veiculo', {})  # Pega o dicionário "Veiculo"

        corrida = {
            'Motorista ID': motorista_id,
            'Motorista': motorista_info.get('Motorista', None),
            'Telefone Motorista': motorista_info.get('Telefone', None),
            'CPF': motorista_info.get('cpf', None),
            'Avaliação Motorista': motorista_info.get('Avaliacao', None),
            'Veículo': {
                'tipo': veiculo.get('Tipo', None), 
                'marca': veiculo.get('modelo', None),
                'ano': veiculo.get('ano', None),
                'placa': veiculo.get('placa', None)
            },
            'Passageiro': dados_passageiro.get('Nome Passageiro', None),
            'Telefone': dados_passageiro.get('Telefone', None),
            'origem': origem, 
            'destino': destino,
            'distancia': self.__distancia,
            'tempo corrida': self.__tempo,
            'valor base': round(self.__valorfinal,2),
            'desconto': round(self.__valordesconto,2),
            'Forma Pagamento': forma_pagamento,
            'valor final':round((self.__valorfinal - self.__valordesconto),2),
            'status': status
        }

        Corrida.adicionar_corrida_motorista(self.__id_corrida, corrida)

        return


    def consultar_corridas_motorista(self, cpf: str) -> None:
        "Consultar dicionário de corridas para um determinado CPF de motorista com retorno de um resumo"

        corridas_correspondentes = {}
        valor_total = 0.0

        # Invoca o método de classe para obter as corridas dos motoristas
        corridas = Corrida.get_corridas_motoristas()

        # Itera sobre todas as corridas
        for id_corrida, dados_corrida in corridas.items():
            # Verifica se o CPF da corrida corresponde ao CPF fornecido
            if dados_corrida.get('CPF') == cpf:
                corridas_correspondentes[id_corrida] = dados_corrida
                # Adiciona o valor final apenas se a corrida foi realizada
                if dados_corrida.get('status') == 'realizada':
                    valor_total += dados_corrida.get('valor final', 0.0)

        if not corridas_correspondentes:
            return '\033[31mDados não localizados\033[m'
        else:
            # Imprime as corridas encontradas de forma organizada
            for id_corrida, dados_corrida in corridas_correspondentes.items():
                print(f"\033[34mCorrida ID: {id_corrida}\nDetalhes: {dados_corrida}\033[m")

            # Imprime o valor total
            print(f"\033[34mValor total das corridas realizadas pelo MOTORISTA selecionado: R$ {valor_total:.2f}\033[m")

        return


    def consulta_corridas_passageiros(self, cpf: str) -> None:
        "Consultar dicionário de corridas para um determinado CPF e retornar a soma dos valores finais das corridas realizadas"

        corridas_correspondentes = {}
        valor_total = 0.0

        # Invoca o método de classe para obter as corridas dos passageiros
        corridas = Corrida.get_corridas_passageiros()

        # Itera sobre todas as corridas
        for id_corrida, dados_corrida in corridas.items():
            # Verifica se o CPF da corrida corresponde ao CPF fornecido
            if dados_corrida.get('CPF') == cpf:
                corridas_correspondentes[id_corrida] = dados_corrida
                # Adiciona o valor final apenas se a corrida foi realizada
                if dados_corrida.get('status') == 'realizada':
                    valor_total += dados_corrida.get('valor final', 0.0)

        if not corridas_correspondentes:
            return '\033[31mDados incorretos ou não localizados\033[m'
        else:
            # Imprime as corridas encontradas de forma organizada
            for id_corrida, dados_corrida in corridas_correspondentes.items():
                print(f"\033[35mCorrida ID: {id_corrida}\nDetalhes: {dados_corrida}\033[m")

            # Imprime o valor total
            print(f"\033[35mValor total das corridas realizadas pelo PASSAGEIRO selecionado: R$ {valor_total:.2f}\033[m")

        return


    def _validar_dados_passageiro(self, **kwargs) ->None:
        "Método de validacao de atributos"
        if 'origem' in kwargs and not isinstance(kwargs['origem'], str):
            raise ValueError("\033[31mDigite um endereço valido\033[m")
        if 'destino' in kwargs and not isinstance(kwargs['destino'], str):
            raise ValueError("\033[31mDigite um endereço valido\033[m")
        if 'categoria' in kwargs:
            categoria = kwargs['categoria'].lower()
            if categoria not in ["luxo", "economica", "economico"]:
                raise ValueError("\033[31mCategoria invalida, digite Luxo ou Economica\033[m")
        if 'forma_pagamento' in kwargs:
            forma_pagamento = kwargs['forma_pagamento'].lower()
            formas_permitidas = ["dinheiro", "cartao", "pix"]
            if forma_pagamento not in formas_permitidas:
                raise ValueError("\033[31mFormas de pagamento disponíveis: DINHEIRO, CARTAO ou PIX\033[m")
        if 'veiculo' in kwargs:
            veiculos = ['carro', 'moto']
            veiculo = kwargs['veiculo'].lower()
            if veiculo not in veiculos:
                raise ValueError('\033[31mOpções disponiveis de veículo: CARRO ou MOTO\033[m')