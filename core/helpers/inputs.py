
from engine.move import Move

def inputHandler(board):                                                                   # Check for the correct input notation
    command = input("Give Command like a2a4q or stop: ")
    if command == "stop":
        board.gamestate.running = False
        return
    elif not isValidMoveFormat(command): 
        print("Invalid command format. Please try again.")
    else:
        print("Valid move input. (Legality not yet checked)")
        return moveParser(command, board)
    
def isValidMoveFormat(command):                            
    if len(command) != 5 and len(command) != 4:
        return False
    if len(command) == 4:  
        return validNonPromotion(command)
    if len(command) == 5:
        return validNonPromotion(command) and validPromotion(command)
        
def validNonPromotion(command):
    return (
        command[0] in "abcdefgh" and
        command[1] in "12345678" and
        command[2] in "abcdefgh" and
        command[3] in "12345678")

def validPromotion(command):
    if command[4] not in "rnbq":
        return False
    return True

def moveParser(move, board):                                                                    # Changes the input to a move
    file_from = ord(move[0]) - ord('a')
    rank_from = int(move[1]) - 1
    file_to = ord(move[2]) - ord('a')
    rank_to = int(move[3]) - 1
    promotion_flag = move[4] if len(move) == 5 else None
    startsquare = rank_from * 8 + file_from
    endsquare = rank_to * 8 + file_to
    parsed_move = Move(startsquare, endsquare).createPlayerMove(board, promotion_flag)
    return parsed_move