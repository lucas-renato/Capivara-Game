from collections import deque
from random import shuffle
from typing import List, Tuple, Deque, Optional

# /c:/LBD/capivara-game/src/__init__.py
# Pequeno motor para iniciar um jogo de dominó (automático, CLI)


Tile = Tuple[int, int]


def make_deck(max_pip: int = 6) -> List[Tile]:
  """Cria o baralho padrão de dominó (double-six por padrão)."""
  return [(i, j) for i in range(max_pip + 1) for j in range(i, max_pip + 1)]


def tile_matches(tile: Tile, number: int) -> bool:
  return tile[0] == number or tile[1] == number


def flip(tile: Tile) -> Tile:
  return (tile[1], tile[0])


class Player:
  def __init__(self, name: str):
    self.name = name
    self.hand: List[Tile] = []

  def playable_tiles(self, left: int, right: int) -> List[Tuple[Tile, str]]:
    """Retorna lista de (tile, side) que podem ser jogadas, side é 'L' ou 'R'."""
    result = []
    for t in self.hand:
      if tile_matches(t, left):
        result.append((t, 'L'))
      if tile_matches(t, right):
        result.append((t, 'R'))
    return result

  def remove_tile(self, tile: Tile):
    self.hand.remove(tile)

  def pip_count(self) -> int:
    return sum(a + b for a, b in self.hand)

  def __str__(self):
    return f"{self.name} ({len(self.hand)} peças)"


class DominoGame:
  def __init__(self, player_names: List[str], max_pip: int = 6, hand_size: int = 7):
    self.players = [Player(n) for n in player_names]
    self.max_pip = max_pip
    self.hand_size = hand_size
    self.boneyard: List[Tile] = []
    self.board: Deque[Tile] = deque()
    self.turn = 0  # índice do jogador atual

  def setup(self):
    deck = make_deck(self.max_pip)
    shuffle(deck)
    # distribuir
    for _ in range(self.hand_size):
      for p in self.players:
        if deck:
          p.hand.append(deck.pop())
    self.boneyard = deck
    # determinar quem inicia: maior duplo; se nenhum, maior soma
    starter, tile = self.find_starting_tile()
    if tile is None:
      # nenhum tile encontrado (improvável), pega do boneyard
      if self.boneyard:
        tile = self.boneyard.pop()
        starter = 0
    # coloca tile na mesa e remove da mão do starter
    if tile:
      self.board.append(tile)
      self.turn = starter
      self.players[starter].remove_tile(tile)

  def find_starting_tile(self) -> Tuple[int, Optional[Tile]]:
    best_tile: Optional[Tile] = None
    best_player = 0
    best_value = -1
    for i, p in enumerate(self.players):
      for t in p.hand:
        if t[0] == t[1]:
          val = t[0] * 2 + 100  # força os duplos a vencerem
        else:
          val = t[0] + t[1]
        if val > best_value:
          best_value = val
          best_tile = t
          best_player = i
    return best_player, best_tile

  def play(self, verbose: bool = True):
    passes_in_row = 0
    if verbose:
      print("Iniciando partida de dominó")
      for p in self.players:
        print(f"{p.name}: {p.hand}")
      print("Mesa inicial:", list(self.board))
      print("Boneyard:", len(self.boneyard), "peças")

    while True:
      player = self.players[self.turn]
      left, right = self.board[0][0], self.board[-1][1]
      playable = player.playable_tiles(left, right)

      if playable:
        # escolha simples: primeiro disponível
        chosen_tile, side = playable[0]
        # ajustar orientação se necessário
        if side == 'L':
          # encaixa com left
          if chosen_tile[1] == left:
            self.board.appendleft(chosen_tile)
          elif chosen_tile[0] == left:
            self.board.appendleft(flip(chosen_tile))
          else:
            # should not happen
            self.board.appendleft(chosen_tile)
        else:  # 'R'
          if chosen_tile[0] == right:
            self.board.append(chosen_tile)
          elif chosen_tile[1] == right:
            self.board.append(flip(chosen_tile))
          else:
            self.board.append(chosen_tile)
        player.remove_tile(chosen_tile)
        passes_in_row = 0
        if verbose:
          print(f"{player.name} joga {chosen_tile} no lado {side} -> Mesa: {list(self.board)}")
        # verifica vitória
        if not player.hand:
          if verbose:
            print(f"{player.name} venceu!")
          return player.name
      else:
        # tenta comprar até conseguir jogar ou boneyard acabar
        drew_and_played = False
        while self.boneyard:
          drawn = self.boneyard.pop()
          player.hand.append(drawn)
          if verbose:
            print(f"{player.name} compra {drawn} (boneyard resta {len(self.boneyard)})")
          # verifica se pode jogar agora
          playable = player.playable_tiles(left, right)
          if playable:
            chosen_tile, side = playable[0]
            if side == 'L':
              if chosen_tile[1] == left:
                self.board.appendleft(chosen_tile)
              elif chosen_tile[0] == left:
                self.board.appendleft(flip(chosen_tile))
              else:
                self.board.appendleft(chosen_tile)
            else:
              if chosen_tile[0] == right:
                self.board.append(chosen_tile)
              elif chosen_tile[1] == right:
                self.board.append(flip(chosen_tile))
              else:
                self.board.append(chosen_tile)
            player.remove_tile(chosen_tile)
            drew_and_played = True
            passes_in_row = 0
            if verbose:
              print(f"{player.name} joga {chosen_tile} após comprar -> Mesa: {list(self.board)}")
            if not player.hand:
              if verbose:
                print(f"{player.name} venceu!")
              return player.name
            break
        if not drew_and_played:
          # passa
          passes_in_row += 1
          if verbose:
            print(f"{player.name} passa")
      # condição de bloqueio: todos passaram em sequência
      if passes_in_row >= len(self.players):
        # jogador com menor soma vence
        winner = min(self.players, key=lambda p: p.pip_count())
        if verbose:
          print("Jogo bloqueado. Resultado por menor pip:")
          for p in self.players:
            print(f"{p.name}: {p.pip_count()} pips")
          print(f"Vencedor: {winner.name}")
        return winner.name
      # próximo turno
      self.turn = (self.turn + 1) % len(self.players)


def start_game(player_names: List[str] = None, max_pip: int = 6, hand_size: int = 7):
  if player_names is None:
    player_names = ["Jogador 1", "Jogador 2"]
  game = DominoGame(player_names, max_pip=max_pip, hand_size=hand_size)
  game.setup()
  return game.play(verbose=True)


if __name__ == "__main__":
  # Exemplo: iniciar jogo automático com 2 jogadores
  start_game(["Alice", "Bot"])