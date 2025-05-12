
from engine.piece import Piece                                                                                                # Example FENs "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2" ,"pn7/8/8/2p5/4P3/8/PPP5/6N1 w KQkq c6 0 2"

def loadFEN(board):
    start_FEN =  "8/8/8/1k1K4/8/8/8/8"#"1b4nR/3P4/7N/pP6/1B6/r7/4P3/8 w KQkq a6 0 2" #"8/8/8/p7/8/8/8/4K2R w KQkq c6 0 2"

    parts = start_FEN.strip().split()                                   # Splitting the FEN string into it's parts 
                                                                        
    piece_placement = parts[0]                                  
    active_color = parts[1] if len(parts) > 1 else 'w'
    castling_rights = parts[2] if len(parts) > 2 else '-'
    en_passant = parts[3] if len(parts) > 3 else '-'
    halfmove_clock = int(parts[4]) if len(parts) > 4 else 0
    fullmove_number = int(parts[5]) if len(parts) > 5 else 1


    rows = piece_placement.split("/")                           # List with pieces ["rnbkqr","pp1ppp",....] seperated by /
    square_index = 0

    for fen_rank_index in range(8):
        rank = 7 - fen_rank_index
        file = 0
        for char in rows[fen_rank_index]:               
            if char.isdigit():                                  # If there is a digit (Blank space in FEN notation) skip those files
                file += int(char)
            else:
                piece = Piece().symbolToPiece(char)             # If there is a piece character transform char to interior piece notation (integer)
                square_index = rank * 8 + file
                board.setPiece(square_index, piece)             # Give the piece and its square index to board.setPiece
                file += 1

    board.gamestate.active_color = 0 if active_color == 'w' else 8                                      # Set the correct gamestate information
    board.gamestate.white_kingsidecastle_rights = 'K' in castling_rights
    board.gamestate.white_queensidecastle_rights = 'Q' in castling_rights
    board.gamestate.black_kingsidecastle_rights = 'k' in castling_rights
    board.gamestate.black_queensidecastle_rights = 'q' in castling_rights
    board.gamestate.enpassant_square = algebraicToIndex(en_passant) if en_passant != '-' else None
    board.gamestate.halfmoves = int(halfmove_clock)
    board.gamestate.fullmoves = int(fullmove_number)
    
def algebraicToIndex(square):                                   # Calcualtes the square index from the en passant square in the FEN string
    if len(square) != 2:
        return None
    file = ord(square[0]) - ord('a')
    rank = int(square[1]) - 1
    return rank * 8 + file
      