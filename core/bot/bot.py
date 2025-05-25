
import numpy as np
from bot.evaltuation import Evaluation


class Bot:
    def __init__(self, player_color):
        self.evaluation = Evaluation()

    def chooseMove(self, board):
        best_score = None
        best_move = None

        for move in board.legal_moves:
            board.makeMove(move)
            score = self.evaluation.pieceCount(board)
            board.undoMove()
            print("Score:" ,score, "for move:" ,move)
 

            if best_score is None or score > best_score:
                best_score = score
                best_move = move

        return best_move
