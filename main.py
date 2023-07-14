import Veiculos
import Pessoas
import Corrida

# #Objetos - CARROS
try:
    carro1 = Veiculos.Carro("RHW1E28", 'Fit', 'Honda', 2013, 'Bege', 4, 5)
    carro2 = Veiculos.Carro("GVJ277H", 'LOGAN', 'Honda', 2015, "Azul", 4, 5)
    carro3 = Veiculos.Carro("HGS3746", 'PUNTO', 'Honda', 2020, "Preto", 5, 5)
except ValueError as e:
    print(f"Erro atributo: {str(e)}")

# #Objetos - MOTOS
try:
    moto1 = Veiculos.Moto("KKS4758", 'CBX', 'Honda', 2015, "Verde", 100)
    moto2 = Veiculos.Moto("MCH1938", 'CG', 'Honda', 2016, "Verde", 200)
    moto3 = Veiculos.Moto("BSH3826", 'HC', 'Honda', 2017, "Azul", 150)
except ValueError as e:
    print(f"Erro atributo: {str(e)}")

# #Objetos - MOTORISTAS
motoristas = [
    ('Pedro Argenta', 49, 992759780, '00600800632', carro1.get_atributos(), '80506020101', 3),
    ('Luan Brasil', 32, 876328405, '73684927364', carro2.get_atributos(), '63547389876', 4),
    ('Joao Paraguai', 24, 982672837, '00293725366', carro3.get_atributos(), '35462734578', 5),
    ('Amanda Argenta', 19, 987153745, '92893476847', moto1.get_atributos(), '82736457283', 4),
    ('Luiza Brasil', 28, 988763514, '01992987644', moto2.get_atributos(), '90376123456', 2),
    ('Aline Paraguai', 30, 766235416, '87887865634', moto3.get_atributos(), '89764523457', 5)
 ]
try:
    for motorista in motoristas:
        motora = Pessoas.Motorista_Cadastro(*motorista)
except ValueError as e:
    print(f"Erro atributo: {str(e)}")

# Instanciar um passageiro
try:
    passageiro = Pessoas.Passageiro("Pedrinho", 20, 333070203, "08004087892", 4)
except ValueError as e:
    print(f"Erro atributo: {str(e)}")
# chamar uma corrida
try:
    passageiro.iniciar_corrida_passageiro("rua da caida", "rua da subida", 'carro', "luxo", 'pix')
except ValueError as e:
    print(f"Erro atributo: {str(e)}")

# consultar as corridas de um passageiro com o CPF
print('\n\033[35mCORRIDAS PASSAGEIRO\033[m')
try:
    passageiro.relatorio_passageiro("08004087892")
except ValueError as e:
        print(f"Erro atributo: {str(e)}")

# consultar a lista de corridas de um motorista pelo CPF
motorista = Corrida.Corrida()
print('\n\033[34mCORRIDAS MOTORISTA\033[m')
try:
    motorista.consultar_corridas_motorista('00293725366')
except ValueError as e:
        print(f"Erro atributo: {str(e)}")

# Instanciar um passageiro
try:
    passageiro = Pessoas.Passageiro("Luana", 30, 988070203, "01004086997", 5)
except ValueError as e:
    print(f"Erro atributo: {str(e)}")

# chamar uma corrida
try:
    passageiro.iniciar_corrida_passageiro("rua A", "rua B", 'carro', "luxo", 'cartao')
except ValueError as e:
    print(f"Erro atributo: {str(e)}")
# chamar uma corrida
try:
    passageiro.iniciar_corrida_passageiro("rua B", "rua A", 'carro', "luxo", 'dinheiro')
except ValueError as e:
    print(f"Erro atributo: {str(e)}")
# chamar uma corrida
try:
    passageiro.iniciar_corrida_passageiro("rua alta", "rua magra", 'moto', "economico", 'pix')
except ValueError as e:
    print(f"Erro atributo: {str(e)}")

# consultar as corridas de um passageiro com o CPF
print('\n\033[35mCORRIDAS PASSAGEIRO\033[m')
try:
    passageiro.relatorio_passageiro("01004086997")
except ValueError as e:
    print(f"Erro atributo: {str(e)}")

# consultar a lista de corridas de um motorista pelo CPF
print('\n\033[34mCORRIDAS MOTORISTA\033[m')
try:
    motorista.consultar_corridas_motorista('00293725366')
except ValueError as e:
    print(f"Erro atributo: {str(e)}")