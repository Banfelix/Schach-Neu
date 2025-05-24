
from engine.board import Board
from helpers.inputs import inputHandler
from helpers.inputs import getPlayerColor
from debugs import moveToAlgebraic




def main():
    board = Board()
    player_color = getPlayerColor()

    print("player_color=", player_color)
    
    first_load = True
    board.loadLegalMoves(first_load)
    move_list = [moveToAlgebraic(move) for move in board.legal_moves]   # For debugging
    print(' || '.join(move_list))
    print("Legal moves:", len(move_list))

    while board.gamestate.running:
        first_load = False

        if board.gamestate.active_color == player_color:
            legal = False
            while not legal:
                move = inputHandler(board) 

                if move is False:
                    print("Game stopped by user.")
                    board.gamestate.running = False
                    break  # Break out of the inner input loop (and outer will exit next cycle)

                elif move is not None:
                    print("Legal move input:", move)
                    board.makeMove(move)
                    board.printBoard()
                    legal = True  # Valid move made, break loop

                else:
                    print("Illegal move or invalid input, try again.")




            board.loadLegalMoves(first_load)
            move_list = [moveToAlgebraic(move) for move in board.legal_moves]   # For debugging
            print(' || '.join(move_list))
            print("Legal moves:", len(move_list))

        else:   # Add bot here later on
            legal = False
            while not legal:
                move = inputHandler(board) 

                if move is False:
                    print("Game stopped by user.")
                    board.gamestate.running = False
                    break  # Break out of the inner input loop (and outer will exit next cycle)

                elif move is not None:
                    print("Legal move input:", move)
                    board.makeMove(move)
                    board.printBoard()
                    legal = True  # Valid move made, break loop

                else:
                    print("Illegal move or invalid input, try again.")




            board.loadLegalMoves(first_load)
            move_list = [moveToAlgebraic(move) for move in board.legal_moves]   # For debugging
            print(' || '.join(move_list))            
            print("Legal moves:", len(move_list))

if __name__ == "__main__":
    main()

    #   cd "C:\Users\User\Desktop\Chess New Movegen"
    #   C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe core\main.py
    #  C:\Users\User\Desktop\Chess New Movegen>C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe -m cProfile -s time core\main.py
    