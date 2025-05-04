
from engine.board import Board
from helpers.inputs import inputHandler



def main():
    board = Board()
    while board.gamestate.running:
        move = inputHandler(board)
        print(move)

if __name__ == "__main__":
    main()