from engine.piece import Piece
from engine.piecelist import PieceList  
from engine.gamestate import GameState
from helpers.fen import loadFEN


class Board:
    def __init__(self):
        self.piece = Piece()
        self.gamestate = GameState()
        self.board = [self.piece.nopiece] * 64
        self.legal_moves = []

        self.piecelists = {                                                     # Dictionnary of all pieces {int of the piece : PieceList Object with occupied squares, amount of those pieces, }
            self.piece.whitepawn: PieceList(),
            self.piece.whiteknight: PieceList(),
            self.piece.whitebishop: PieceList(),
            self.piece.whiterook: PieceList(),
            self.piece.whitequeen: PieceList(),
            self.piece.whiteking: PieceList(),
            self.piece.blackpawn: PieceList(),
            self.piece.blackknight: PieceList(),
            self.piece.blackbishop: PieceList(),
            self.piece.blackrook: PieceList(),
            self.piece.blackqueen: PieceList(),
            self.piece.blackking: PieceList()}

        self.loadGame()
        self.printBoard()

    def loadGame(self):
        loadFEN(self)

    def printBoard(self):
        for rank in range(7, -1, -1):  
            row = f"{rank + 1}    "  
            for file in range(8):
                square_index = rank * 8 + file
                piece = self.board[square_index]
                symbol = self.piece.pieceToSymbol(piece) if piece else "-"
                row += symbol + " "
            print(row)
        print("\n","    a b c d e f g h")


    def setPiece(self, square, piece):                                          # Gets two ints, a square index and a piece number
        old_piece = self.board[square]                                          # Checks what piece is at the given square
        if old_piece != self.piece.nopiece:                                     # If there is a piece remove it
            self.piecelists[old_piece].removePiece(square)                      # Used in FEN to setup the board from a FEN string

        self.board[square] = piece
        if piece != self.piece.nopiece:
            self.piecelists[piece].addPiece(square)

    def makeMove(self, move):
        moving_piece = self.board[move.start_square]                                                                   # Get the int of the moving piece and captured piece -> see Pieces for more
        captured_piece = self.board[move.end_square]    
        
        if captured_piece != self.piece.nopiece:
            self.piecelists[captured_piece].removePiece(move.end_square)                                               # Remove captured piece
        
        self.piecelists[moving_piece].removePiece(move.start_square)                                                   # Update piecelists: move the moving piece
        self.piecelists[moving_piece].addPiece(move.end_square)

        self.board[move.end_square] = moving_piece                                                                     # Update The board for visual representation
        self.board[move.start_square] = self.piece.nopiece
        
        self.gamestate.active_color ^= 1                                                                               # Change side to play
