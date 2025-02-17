# Dots and Boxes AI

This repository contains AI implementations for the classic **Dots and Boxes** game using three different strategies:

- **Minimax Algorithm** (minimax.py)
- **Alpha-Beta Pruning** (alpha_beta_prun.py)
- **Monte Carlo Tree Search (MCTS)** (monte_carlo.py)

## AI Strategies
- **Minimax:** Exhaustively searches the game tree to find the optimal move.
- **Alpha-Beta Pruning:** An optimization of Minimax that eliminates unnecessary branches, improving efficiency.
- **MCTS:** Uses random simulations to determine the best move based on probabilistic evaluations.

## File Structure
```
Ai_assignment/
│── alpha_beta_prun.py   # Alpha-Beta Pruning implementation
│── minimax.py           # Minimax Algorithm implementation
│── monte_carlo.py       # Monte Carlo Tree Search implementation
│── calc.py              # Calculates the search space given the board size
```
