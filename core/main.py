
from engine.board import Board
from helpers.inputs import inputHandler
from movegeneration.movegenerator import MoveGenerator
from debugs import moveToAlgebraic

def main():
    board = Board()
    while board.gamestate.running:
        move = inputHandler(board)                          # Returns move in internal notation
        if move:print(bin(move))
        MoveGenerator(board).getRookMoves(board)
        MoveGenerator(board).getPawnMoves(board)
        for move in board.legal_moves:
            moveToAlgebraic(move)

if __name__ == "__main__":
    main()