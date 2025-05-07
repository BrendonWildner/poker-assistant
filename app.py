import streamlit as st
from poker_engine import decide_poker_move

st.set_page_config(page_title="Poker Assistant", layout="centered")
st.title("Assistente de Jogada de Poker")

# Guia de Naipes
st.markdown(
    "**Guia de Naipes:**\n"
    "- s: Espadas (♠)\n"
    "- h: Copas (♥)\n"
    "- d: Ouros (♦)\n"
    "- c: Paus (♣)"
)

# 1. Seletor de estágio (pré-flop, flop, turn, river)
stage = st.selectbox("Situação da mão", ["Pré-Flop", "Flop", "Turn", "River"])

# Função para gerar todas as cartas possíveis
def format_cards():
    ranks = ['A','K','Q','J','T','9','8','7','6','5','4','3','2']
    suits = ['s','h','d','c']
    return [r + s for r in ranks for s in suits]

cards = format_cards()

# 2. Seleção de cartas do usuário
col1, col2 = st.columns(2)
with col1:
    card1 = st.selectbox("Carta 1", cards)
with col2:
    card2 = st.selectbox("Carta 2", cards)

# 3. Cartas do board (dinâmico conforme estágio)
if stage != "Pré-Flop":
    board = st.multiselect(
        "Cartas no bordo", cards,
        help="Selecione de 3 a 5 cartas conforme o estágio"
    )
else:
    board = []

# 4. Inputs numéricos para parâmetros de jogo
df = st.number_input  # placeholder para alinhamento
total_players = st.number_input("Número de jogadores ativos", min_value=2, max_value=10, value=6)
pot = st.number_input("Tamanho do pote", min_value=0, value=100, step=10)
call = st.number_input("Custo do call", min_value=0, value=20, step=5)
stack = st.number_input("Tamanho de stack efetivo", min_value=0, value=200, step=10)

# 5. Botão para calcular e exibir recomendação
if st.button("👉 Sugira minha ação"):
    action, justification = decide_poker_move([card1, card2], board, total_players, pot, call, stack)
    if action == 'fold':
        st.error(f"**FOLD**\n{justification}")
    elif action == 'call':
        st.warning(f"**CALL**\n{justification}")
    else:
        st.success(f"**RAISE**\n{justification}")