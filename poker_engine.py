import random
from treys import Card, Evaluator, Deck


def estimate_equity(hole_cards, board_cards, num_opponents, n_iterations=5000):
    evaluator = Evaluator()
    wins = ties = 0

    hole = [Card.new(c) for c in hole_cards]
    board = [Card.new(c) for c in board_cards]

    for _ in range(n_iterations):
        deck = Deck()
        for c in hole + board:
            deck.cards.remove(c)

        opp_hands = [[deck.draw(1)[0], deck.draw(1)[0]] for _ in range(num_opponents)]
        sim_board = board.copy()
        while len(sim_board) < 5:
            sim_board.append(deck.draw(1)[0])

        user_score = evaluator.evaluate(sim_board, hole)
        opp_scores = [evaluator.evaluate(sim_board, h) for h in opp_hands]

        if user_score < min(opp_scores):
            wins += 1
        elif user_score == min(opp_scores):
            ties += 1

    total = n_iterations
    return (wins + ties * 0.5) / total


def decide_poker_move(hole_cards, board_cards, num_players, pot_size, call_amount, stack_size):
    num_opponents = num_players - 1
    equity = estimate_equity(hole_cards, board_cards, num_opponents)
    pot_odds = call_amount / (pot_size + call_amount) if (pot_size + call_amount) else 1

    if equity < pot_odds:
        return 'fold', f'Equity {equity:.1%} < pot odds {pot_odds:.1%} → fold'
    if equity > pot_odds + 0.10:
        raise_size = pot_size * 0.75
        return 'raise', f'Equity {equity:.1%} > pot odds {pot_odds:.1%} → raise {raise_size:.0f}'
    return 'call', f'Equity {equity:.1%} ≈ pot odds {pot_odds:.1%} → call'