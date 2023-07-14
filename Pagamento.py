

class Pagamento:
    "Classe para processar e devolver os valores de pagamentos"


    def valores_corrida(self, distancia:int, tempo:int, categoria:str, forma_pagamento:str) -> float:
        "Método para calcular os valores bases, descontos conforme método de pagamento e valor final"
        taxa_quilometro = 2.5
        taxa_minuto = 0.5
        valor_base = distancia * taxa_quilometro + tempo * taxa_minuto
        valor_final = valor_base

        categoria = categoria.lower()
        if categoria == 'luxo':
            valor_final = valor_base * 1.5

        forma_pagamento = forma_pagamento.lower()
        if forma_pagamento == 'pix':
            desconto = valor_final * 0.1
        elif forma_pagamento == 'cartao':
            desconto = valor_final * 0.05
        else:
            desconto = 0.0

        return [round(valor_final,2), round(desconto,2)]

