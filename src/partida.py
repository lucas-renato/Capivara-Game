from src.utils import gerar_pecas
from src.jogador import Jogador

class Partida:
    def __init__(self):
        self.pecas = gerar_pecas()
        self.mesa = []
        self.jogadores = [
            Jogador("Jogador 1"),
            Jogador("Jogador 2")
        ]

    def distribuir(self):
        for jogador in self.jogadores:
            mao = [self.pecas.pop() for _ in range(7)]
            jogador.receber_pecas(mao)

    def mostrar_mesa(self):
        if not self.mesa:
            return "(vazia)"
        return " ".join(str(p) for p in self.mesa)

    def iniciar(self):
        print("=== Iniciando o Capivara Game ===\n")
        self.distribuir()
        print("Mesa:", self.mostrar_mesa())

        for jogador in self.jogadores:
            print(f"{jogador.nome}: {jogador.mostrar_mao()}")
