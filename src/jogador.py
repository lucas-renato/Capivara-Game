class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.mao = []

    def receber_pecas(self, pecas):
        self.mao = pecas

    def jogar_peca(self, indice):
        return self.mao.pop(indice)

    def mostrar_mao(self):
        return " ".join(str(p) for p in self.mao)
