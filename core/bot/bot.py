
import numpy as np
from bot.evaluation import Evaluation
from engine.move import Move


class Bot:
    def __init__(self, player_color):
        self.evaluation = Evaluation()
        self.depth = 3
        self.player_color = player_color
        self.nodes = 0

    def search(self, board):
        self.nodes = 0
        color = 1 if board.gamestate.active_color == self.player_color else -1
        score, best_move = self.negamax(board, self.depth, color)
        print(f"Search completed. Best move: {best_move}, Score: {score}, Nodes searched: {self.nodes}")
        return best_move


    def negamax(self, board, depth, color):
        self.nodes += 1
        print("Node:" ,self.nodes)
        if depth == 0 or not board.gamestate.running:
            print("Reached depth of 0")
            return color * self.evaluation.pieceCount(board), None

        max_score = -self.evaluation.max_value
        best_move = None

        for move in board.legal_moves:
            
            print(f"wants to move from {(move&0b0000000000111111)} to {(move&0b0000111111000000)>>6}")
            board.makeMove(move)


            score, _ = self.negamax(board, depth - 1, -color)
            score = -score
            
        
            board.unMakeMove()
            print("unmake is called, board after unmake:")
            board.printBoard()
            
            if score > max_score:
                max_score = score
                best_move = move

        print("best move: ",best_move,"   best score: ", max_score)
        return max_score, best_move

