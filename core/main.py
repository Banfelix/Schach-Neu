
from engine.board import Board
from helpers.inputs import inputHandler
from debugs import moveToAlgebraic

def main():
    board = Board()
    while board.gamestate.running:
        board.loadLegalMoves()
        move_list = [moveToAlgebraic(move) for move in board.legal_moves]   # For debugging
        print(' || '.join(move_list))

        move = inputHandler(board)                          # Returns move in internal notation
        if move is not None:
            print("Legal move", move)
            print("make the move, update boardstate")
            board.makeMove(move)
        else:
            print("Illegal move, try again.")


if __name__ == "__main__":
    main()