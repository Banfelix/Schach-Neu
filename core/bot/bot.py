
import numpy as np
from bot.evaluation import Evaluation
import random
import os
from debugs import moveToAlgebraic
from helpers.fen import getFEN

class Bot:
    def __init__(self, player_color):
        self.evaluation = Evaluation()
        self.depth = 3
        self.player_color = player_color
        self.nodes = 0
        self.opening_book = self.loadOpeningBook("black_positions.txt") if self.player_color == 0 else self.loadOpeningBook("white_positions.txt")


    def loadOpeningBook(self, filename):
        base_path = os.path.abspath(os.path.dirname(__file__))  # path to bot.py
        book_path = os.path.join(base_path, "..", "..", "assets", filename)
        book = {}
        with open(book_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    fen = " ".join(parts[:6])
                    moves = parts[6:]
                    book[fen] = moves
        return book


    def search(self, board):
        print("Searching...")
        self.nodes = 0
        if board.gamestate.fullmoves <= 6:
            move = self.openingBookMove(board)
            if move: return move
            
        color = 1 if board.gamestate.active_color == self.player_color else -1
        score, best_move = self.negamax(board, self.depth, color)
        print(f"Search completed. Best move: {best_move}, Score: {score}, Nodes searched: {self.nodes}")
        return best_move


    def negamax(self, board, depth, color):
        self.nodes += 1
        if depth == 0 or not board.gamestate.running:
            return color * self.evaluation.pieceCount(board), None

        max_score = -self.evaluation.max_value
        best_moves = []

        moves = list(board.legal_moves)
        for move in moves:
            board.makeMove(move)

            score, _ = self.negamax(board, depth - 1, -color)
            score = -score

            board.unMakeMove()

            if score > max_score:
                max_score = score
                best_moves = [move]  # New best move
            elif score == max_score:
                best_moves.append(move)  # Equal-best move

        # Pick one of the best moves at random
        best_move = random.choice(best_moves) if best_moves else None
        return max_score, best_move
    
    def openingBookMove(self, board):
        fen = getFEN(board)
        if fen in self.opening_book:
            move_choices = self.opening_book[fen]
            chosen = random.choice(move_choices)
            for move in board.legal_moves:
                algebraic_move = moveToAlgebraic(move)
                if algebraic_move == chosen:  # Or moveToAlgebraic(move) if that's your format
                    print(f"Book move chosen: {chosen}")
                    return move
            print(f"Move {chosen} not found in opening book")
        return False


    def loadOpeningBook(self, filename):
        base_path = os.path.abspath(os.path.dirname(__file__))  # path to bot.py
        book_path = os.path.join(base_path, "..", "..", "assets", filename)

        book = {}
        with open(book_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    fen = " ".join(parts[:4])
                    moves = parts[4:]
                    book[fen] = moves
        return book