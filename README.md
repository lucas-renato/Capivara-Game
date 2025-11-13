# 🐾 Capivara Game – Dominó  

**Capivara Game** é um sistema de simulação do jogo de **Dominó**, desenvolvido em **Python** com integração ao **PostgreSQL**.  
O objetivo é permitir partidas automatizadas entre jogadores, com controle de pontuação, histórico e ranking geral.
---

## 🎮 Sobre o projeto

O jogo segue as regras tradicionais do dominó: 28 peças numeradas de 0 a 6, partidas com 2 a 4 jogadores (duplas quando há 4), e vitória ao atingir **50 pontos**.  
As regras de pontuação e encerramento de partida (bater ou trancar o jogo) são aplicadas automaticamente pelo sistema.

O banco de dados é responsável por armazenar usuários, partidas, jogadas e resultados. Parte da lógica do jogo — como validação de jogadas, cálculo de pontos e detecção de jogo trancado — é feita diretamente via **funções e gatilhos SQL**.

---

## 🧱 Tecnologias

- **Python 3.14.0**
- **PostgreSQL**
- **psycopg2** – integração com o banco  
- **python-dotenv** – variáveis de ambiente  
- **prettytable** – visualização no terminal  
---

## ⚙️ Funcionalidades

- Criação e gerenciamento de jogadores  
- Registro de partidas e jogadas  
- Distribuição automática das peças  
- Cálculo de pontuação no banco de dados  
- Ranking de jogadores e histórico de jogos  
- Interação 100% via terminal  

---

## 🚀 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/lucas-renato/capivara-game.git
   cd capivara-game
