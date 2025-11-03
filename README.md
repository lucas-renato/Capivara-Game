# 🐾 Capivara Game – Dominó  
**Disciplina:** Laboratório de Banco de Dados – UFMS  
**Desenvolvido em:** Python + PostgreSQL  

---

## 🧩 Sobre o projeto

O **Capivara Game** é um sistema de gerenciamento para o jogo **Dominó**, desenvolvido como trabalho prático da disciplina **Laboratório de Banco de Dados (UFMS)**.  
O objetivo é modelar e implementar um **banco de dados relacional** capaz de armazenar usuários, partidas, jogadas e pontuações, aplicando regras de negócio diretamente no banco via **funções, gatilhos e procedimentos SQL**.

O sistema funciona totalmente via **linha de comando (console)**, sem interface gráfica ou web.

---

## 🎯 Objetivos do trabalho

- Criar e popular um banco de dados relacional no **PostgreSQL**.  
- Implementar regras de negócio no banco, utilizando:
  - **Triggers (gatilhos)** para cálculo de pontos automáticos;
  - **Procedures (procedimentos)** para compra de peças e validação de jogadas;
  - **Functions (funções)** para verificar jogadas possíveis e detectar jogo trancado;
  - **Views (visões)** para ranking de pontuação e histórico de partidas.  
- Conectar o banco a uma aplicação em **Python**, que simula as partidas e interage com o banco.

---

## 🧱 Tecnologias utilizadas

- **Python 3.x**
- **PostgreSQL 12+**
- **Bibliotecas principais:**
  - `psycopg2` → conexão com o banco de dados  
  - `dotenv` → gerenciamento das variáveis de ambiente  
  - `prettytable` → exibição formatada no console  

---

## ⚙️ Funcionalidades implementadas

- Criação automática das tabelas e povoamento inicial  
- Cadastro de usuários e controle de múltiplas partidas  
- Registro de todas as jogadas realizadas  
- Cálculo automático da pontuação ao bater ou trancar o jogo  
- Detecção de jogo trancado  
- Views para:
  - **Ranking geral** (por jogador)  
  - **Histórico de partidas e vencedores**  

---
