from src.domino import Peca
import random

def gerar_pecas():
    """Gera todas as 28 peças do dominó."""
    pecas = [Peca(i, j) for i in range(7) for j in range(i, 7)]
    random.shuffle(pecas)
    return pecas
