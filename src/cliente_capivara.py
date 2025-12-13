# ============================
# parte 1: infra / banco de dados
# arquivo sugerido: db.py
# ============================

import os
import psycopg2

DBNAME = os.getenv("CAPIVARA_DB", "capivara")
DBUSER = os.getenv("CAPIVARA_USER", "postgres")
DBPASS = os.getenv("CAPIVARA_PASS", "postgres")
DBHOST = os.getenv("CAPIVARA_HOST", "localhost")
DBPORT = os.getenv("CAPIVARA_PORT", "5433")

DSN = (
    f"dbname={DBNAME} "
    f"user={DBUSER} "
    f"password={DBPASS} "
    f"host={DBHOST} "
    f"port={DBPORT}"
)

def get_conn():
    return psycopg2.connect(DSN)


# ============================
# parte 2: lógica de simulação
# arquivo sugerido: simulator.py
# ============================

import random
import time
from db import get_conn


class Simulator:
    def __init__(self, n_players=4, seed=None):
        assert n_players in (2, 3, 4), "n_players must be 2, 3 or 4"
        self.n_players = n_players
        self.users = []
        self.jogo_id = None
        self.partida_id = None

        if seed is None:
            seed = int(time.time())
        random.seed(seed)

    # ---------- setup inicial ----------
    def setup(self):
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SET search_path TO capivara, public;")

            print("criando usuários de simulação...")
            self._create_users(cur)
            self._create_jogo(cur)

            conn.commit()

    def _create_users(self, cur):
        for i in range(self.n_players):
            nome = f"Bot_{i+1}_{random.randint(1000,9999)}"
            email = f"{nome.lower()}@sim.local"

            cur.execute(
                "INSERT INTO usuario (nome,email) VALUES (%s,%s) RETURNING usuario_id",
                (nome, email)
            )
            uid = cur.fetchone()[0]
            self.users.append((uid, nome))
            print(f"  - {nome} (id={uid}) criado")

    def _create_jogo(self, cur):
        cur.execute(
            "INSERT INTO jogo (nome) VALUES (%s) RETURNING jogo_id",
            (f"Jogo_Simulacao_{random.randint(1,999)}",)
        )
        self.jogo_id = cur.fetchone()[0]
        print(f"jogo criado: id={self.jogo_id}")

    # ---------- partida ----------
    def start_partida(self):
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SET search_path TO capivara, public;")

            print("iniciando partida...")
            cur.execute("SELECT iniciar_partida(%s)", (self.jogo_id,))
            self.partida_id = cur.fetchone()[0]

            print(f"partida iniciada: id={self.partida_id}")
            self._vincular_jogadores(cur)
            self._distribuir_pecas(cur)

            conn.commit()

    def _vincular_jogadores(self, cur):
        pos = 1
        dupla = 1

        for uid, nome in self.users:
            cur.execute(
                """
                INSERT INTO jogador (partida_id, usuario_id, posicao, dupla)
                VALUES (%s,%s,%s,%s) RETURNING jogador_id
                """,
                (self.partida_id, uid, pos, dupla)
            )
            jid = cur.fetchone()[0]
            print(f"  - jogador {jid} vinculado ao usuário {nome}")

            pos += 1
            if self.n_players == 4:
                dupla = 1 if dupla == 2 else 2
            else:
                dupla = ((pos - 1) % 2) + 1

    def _distribuir_pecas(self, cur):
        print("distribuindo peças...")
        cur.execute("SELECT distribuir_pecas(%s)", (self.partida_id,))
        print("peças distribuídas.")

    # ---------- simulação ----------
    def simulate_turns(self, max_rounds=500, pause=0):
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SET search_path TO capivara, public;")

            order = self._load_turn_order(cur)
            idx = 0
            rounds = 0

            print("iniciando simulação...")

            while rounds < max_rounds:
                if self._is_partida_encerrada(cur):
                    print("partida encerrada.")
                    break

                jogador_id = order[idx]
                self._executar_turno(cur, jogador_id)

                conn.commit()
                idx = (idx + 1) % len(order)
                rounds += 1

                if pause:
                    time.sleep(pause)

            print(f"simulação finalizada em {rounds} rodadas.")

    def _load_turn_order(self, cur):
        cur.execute(
            "SELECT jogador_id FROM jogador WHERE partida_id=%s ORDER BY posicao",
            (self.partida_id,)
        )
        return [row[0] for row in cur.fetchall()]

    def _is_partida_encerrada(self, cur):
        cur.execute(
            "SELECT estado FROM partida WHERE partida_id=%s",
            (self.partida_id,)
        )
        return cur.fetchone()[0] == "encerrada"

    def _executar_turno(self, cur, jogador_id):
        cur.execute(
            "SELECT * FROM pecas_possiveis(%s,%s)",
            (self.partida_id, jogador_id)
        )
        possiveis = cur.fetchall()

        if possiveis:
            peca_id, _, _ = random.choice(possiveis)
            lado = random.choice(["esquerda", "direita"])
            print(f"Jogador {jogador_id} joga peça {peca_id}")

            cur.execute(
                "SELECT validar_jogada_e_executar(%s,%s,%s,%s)",
                (self.partida_id, jogador_id, peca_id, lado)
            )
        else:
            print(f"Jogador {jogador_id} compra peça")
            cur.execute(
                "SELECT comprar_peca(%s,%s)",
                (self.partida_id, jogador_id)
            )

    # ---------- resumo ----------
    def show_summary(self):
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SET search_path TO capivara, public;")

            print("\nResumo da Partida:")
            cur.execute(
                """
                SELECT partida_id, estado, data_inicio, data_fim
                FROM partida WHERE partida_id=%s
                """,
                (self.partida_id,)
            )
            print(cur.fetchone())

            print("\nPontuação:")
            cur.execute(
                """
                SELECT dupla, pontos
                FROM pontuacao_partida
                WHERE partida_id=%s
                """,
                (self.partida_id,)
            )
            for dupla, pontos in cur.fetchall():
                print(f"Dupla {dupla}: {pontos} pontos")


# ---------- runner ----------

def run_simulation(n_players=4):
    sim = Simulator(n_players)
    sim.setup()
    sim.start_partida()
    sim.simulate_turns()
    sim.show_summary()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Simulador Capivara")
    parser.add_argument("--players", type=int, default=4, choices=[2, 3, 4])
    args = parser.parse_args()

    run_simulation(args.players)
