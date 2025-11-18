class Peca:
    def __init__(self, lado1, lado2):
        self.lado1 = lado1
        self.lado2 = lado2

    def __repr__(self):
        # Representação visual da peça, ex: [6|3]
        return f"[{self.lado1}|{self.lado2}]"

    def inverter(self):
        # Troca os lados da peça
        self.lado1, self.lado2 = self.lado2, self.lado1
    def soma_lados(self):
        # Retorna a soma dos valores dos dois lados
        return self.lado1 + self.lado2      
    def eh_dupla(self):
