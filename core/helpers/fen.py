
from engine.piece import Piece                                                     

def loadFEN(board, fen_string):
    start_FEN = fen_string
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
                piece = board.piece.symbolToPiece(char)             # If there is a piece character transform char to interior piece notation (integer)
                square_index = rank * 8 + file
                board.setPiece(square_index, piece)             # Give the piece and its square index to board.setPiece
                file += 1

    if active_color == "w":
        board.gamestate.inactive_color = 8
        board.gamestate.active_color = 0
    else:  
        board.gamestate.inactive_color = 0
        board.gamestate.active_color = 8                                    # Set the correct gamestate information
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


def getFEN(board):
    piece_map = {
        board.piece.whitepawn: 'P', board.piece.whiteknight: 'N',
        board.piece.whitebishop: 'B', board.piece.whiterook: 'R',
        board.piece.whitequeen: 'Q', board.piece.whiteking: 'K',
        board.piece.blackpawn: 'p', board.piece.blackknight: 'n',
        board.piece.blackbishop: 'b', board.piece.blackrook: 'r',
        board.piece.blackqueen: 'q', board.piece.blackking: 'k',
        board.piece.nopiece: ''
    }

    # 1. Piece placement
    rows = []
    for rank in range(7, -1, -1):
        row = ''
        empty = 0
        for file in range(8):
            square = rank * 8 + file
            piece = board.board[square]
            if piece == board.piece.nopiece:
                empty += 1
            else:
                if empty > 0:
                    row += str(empty)
                    empty = 0
                row += piece_map.get(piece, '?')
        if empty > 0:
            row += str(empty)
        rows.append(row)
    board_part = "/".join(rows)

    # 2. Active color
    color_part = 'w' if board.gamestate.active_color == 0 else 'b'

    # 3. Castling rights
    rights = ''
    if board.gamestate.white_kingsidecastle_rights:
        rights += 'K'
    if board.gamestate.white_queensidecastle_rights:
        rights += 'Q'
    if board.gamestate.black_kingsidecastle_rights:
        rights += 'k'
    if board.gamestate.black_queensidecastle_rights:
        rights += 'q'
    castling_part = rights if rights else '-'

    # 4. En passant target
    ep_part = "-"


    return f"{board_part} {color_part} {castling_part} {ep_part}"
