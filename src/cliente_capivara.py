import os
import random
import time
import psycopg2

DBNAME = os.getenv("CAPIVARA_DB", "capivara")
DBUSER = os.getenv("CAPIVARA_USER", "postgres")
DBPASS = os.getenv("CAPIVARA_PASS", "postgres")
DBHOST = os.getenv("CAPIVARA_HOST", "localhost")
DBPORT = os.getenv("CAPIVARA_PORT", "5433")

DSN = f"dbname={DBNAME} user={DBUSER} password={DBPASS} host={DBHOST} port={DBPORT}"

def get_conn():
    return psycopg2.connect(DSN)

class Simulator:
    def __init__(self, n_players=4, seed=None):
        assert n_players in (2, 3, 4), "n_players must be 2,3 or 4"
        self.n_players = n_players
        if seed is None:
            seed = int(time.time())
        random.seed(seed)
        self.users = []
        self.jogo_id = None
        self.partida_id = None

    def setup(self):
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SET search_path TO capivara, public;")

                print("criando usuários de simulação...")
                for i in range(self.n_players):
                    nome = f"Bot_{i+1}_{random.randint(1000,9999)}"
                    email = f"{nome.lower()}@sim.local"
                    cur.execute(
                        "INSERT INTO usuario (nome,email) VALUES (%s,%s) RETURNING usuario_id",
                        (nome,email)
                    )
                    uid = cur.fetchone()[0]
                    self.users.append((uid,nome))
                    print(f"  - {nome} (id={uid}) criado")

                cur.execute(
                    "INSERT INTO jogo (nome) VALUES (%s) RETURNING jogo_id",
                    (f'Jogo_Simulacao_{random.randint(1,999)}',)
                )
                self.jogo_id = cur.fetchone()[0]
                conn.commit()
                print(f"jogo criado: id={self.jogo_id}")

    def start_partida(self):
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SET search_path TO capivara, public;")

                print("iniciando partida...")
                cur.execute("SELECT iniciar_partida(%s)", (self.jogo_id,))
                self.partida_id = cur.fetchone()[0]
                print(f"partida iniciada: id={self.partida_id}")

                pos = 1
                dupla = 1
                for uid, nome in self.users:
                    cur.execute("""
                        INSERT INTO jogador (partida_id, usuario_id, posicao, dupla)
                        VALUES (%s,%s,%s,%s) RETURNING jogador_id
                    """, (self.partida_id, uid, pos, dupla))
                    jid = cur.fetchone()[0]
                    print(f"  - jogador {jid} vinculado ao usuário {nome}")
                    pos += 1
                    if self.n_players == 4:
                        dupla = 1 if dupla==2 else 2
                    else:
                        dupla = ((pos - 1) % 2) + 1

                print("distribuindo peças...")
                cur.execute("SELECT distribuir_pecas(%s)", (self.partida_id,))
                conn.commit()
                print("peças distribuídas.")

    def simulate_turns(self, max_rounds=500, pause=0):
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SET search_path TO capivara, public;")

                cur.execute("""
                    SELECT jogador_id FROM jogador 
                    WHERE partida_id=%s ORDER BY posicao
                """, (self.partida_id,))
                order = [row[0] for row in cur.fetchall()]
                idx = 0
                rounds = 0

                print("iniciando simulação...")

                while rounds < max_rounds:
                    jogador_id = order[idx]

                    cur.execute("SELECT estado FROM partida WHERE partida_id=%s", (self.partida_id,))
                    if cur.fetchone()[0] == 'encerrada':
                        print("partida encerrada.")
                        break

                    cur.execute("SELECT * FROM pecas_possiveis(%s,%s)", (self.partida_id, jogador_id))
                    poss = cur.fetchall()

                    if poss:
                        peca_id, a, b = random.choice(poss)
                        lado = random.choice(['esquerda','direita'])
                        print(f"Jogador {jogador_id} joga peça {peca_id}")
                        cur.execute(
                            "SELECT validar_jogada_e_executar(%s,%s,%s,%s)",
                            (self.partida_id, jogador_id, peca_id, lado)
                        )
                    else:
                        cur.execute("SELECT comprar_peca(%s,%s)", (self.partida_id, jogador_id))
                        print(f"Jogador {jogador_id} compra peça.")

                    conn.commit()

                    idx = (idx + 1) % len(order)
                    rounds += 1
                    if pause:
                        time.sleep(pause)

                print(f"simulação finalizada em {rounds} rodadas.")

    def show_summary(self):
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SET search_path TO capivara, public;")

                print("\nResumo da Partida:")
                cur.execute("""
                    SELECT partida_id, estado, data_inicio, data_fim 
                    FROM partida WHERE partida_id=%s
                """, (self.partida_id,))
                print(cur.fetchone())

                print("\nPontuação:")
                cur.execute("""
                    SELECT dupla, pontos FROM pontuacao_partida
                    WHERE partida_id=%s
                """, (self.partida_id,))
                for d,p in cur.fetchall():
                    print(f"Dupla {d}: {p} pontos")

def run_simulation(n_players=4):
    sim = Simulator(n_players)
    sim.setup()
    sim.start_partida()
    sim.simulate_turns()
    sim.show_summary()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simulador Capivara')
    parser.add_argument('--players', type=int, default=4, choices=[2,3,4])
    args = parser.parse_args()
    run_simulation(args.players)

if __name__ == '__main__':
    run_simulation(4)           # Executa a simulação com 4 jogadores por padrão
    run_simulation(2)           # Executa a simulação com 2 jogadores
    run_simulation(3)           # Executa a simulação com 3 jogadores
    run_simulation(4)           # Executa a simulação com 4 jogadores novamente
        