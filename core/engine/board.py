from engine.piece import Piece
from engine.piecelist import PieceList  
from engine.gamestate import GameState
from engine.move import Move
from helpers.fen import loadFEN
from movegeneration.movegenerator import MoveGenerator

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

    def loadLegalMoves(self):
        self.legal_moves.clear()
        MoveGenerator(self)


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

    def castleMoveRook(self, from_sq, to_sq):
        rook = self.board[from_sq]
        self.board[to_sq] = rook
        self.board[from_sq] = self.piece.nopiece
        self.piecelists[rook].movePiece(from_sq, to_sq)

    def enPassantHandler(self, moving_piece, end_square):
        if self.piece.getPieceColor(moving_piece) == self.piece.white:
            capture_square = end_square - 8
            print("Capture_square:", capture_square)
        else:
            capture_square = end_square + 8
        captured_piece = self.board[capture_square]
        self.board[capture_square] = self.piece.nopiece
        self.piecelists[captured_piece].removePiece(capture_square)
    
    def castleHandler(self, end_square):
        if end_square == 6:   # White kingside
            self.castleMoveRook(7, 5)
        elif end_square == 2: # White queenside
            self.castleMoveRook(0, 3)
        elif end_square == 62:  # Black kingside
                self.castleMoveRook(63, 61)
        elif end_square == 58:  # Black queenside
                self.castleMoveRook(56, 59)  

    def promotionHandler(self, moving_piece, start_square, end_square, flag):
        color = self.piece.getPieceColor(moving_piece)
        if flag == Move.rook_promotion_flag:
            promoted = self.piece.whiterook if color == self.piece.white else self.piece.blackrook
        elif flag == Move.bishop_promotion_flag:
            promoted = self.piece.whitebishop if color == self.piece.white else self.piece.blackbishop
        elif flag == Move.knight_promotion_flag:
            promoted = self.piece.whiteknight if color == self.piece.white else self.piece.blackknight
        elif flag == Move.queen_promotion_flag:
            promoted = self.piece.whitequeen if color == self.piece.white else self.piece.blackqueen

            self.piecelists[moving_piece].removePiece(start_square)
            self.piecelists[promoted].addPiece(end_square)
            self.board[end_square] = promoted
            self.board[start_square] = self.piece.nopiece        

    def doublePushHandler(self, moving_piece, end_square):
        if self.piece.getPieceColor(moving_piece) == self.piece.white:
            self.gamestate.enpassant_square = end_square - 8
        else:
            self.gamestate.enpassant_square = end_square + 8



    def makeMove(self, move):
        start_square, end_square, flag = Move.moveDecode(move)
        moving_piece = self.board[start_square]
        captured_piece = self.board[end_square]
        
        if flag == Move.en_passant_flag:
            self.enPassantHandler(moving_piece, end_square)
        elif captured_piece != self.piece.nopiece:
            self.piecelists[captured_piece].removePiece(end_square)

        if flag == Move.double_push_flag:
            self.doublePushHandler(moving_piece, end_square)
        else:
            self.gamestate.enpassant_square = None
        
        if flag == Move.castling_flag:
            self.castleHandler(end_square)

        
        if flag in {
            Move.rook_promotion_flag, Move.bishop_promotion_flag,
            Move.knight_promotion_flag, Move.queen_promotion_flag
        }:
            self.promotionHandler(moving_piece, start_square, end_square, flag)
        
        else:
            
            self.piecelists[moving_piece].removePiece(start_square)
            self.piecelists[moving_piece].addPiece(end_square)
            self.board[end_square] = moving_piece
            self.board[start_square] = self.piece.nopiece



        if self.gamestate.active_color == 0:
            self.gamestate.active_color = 8
        else:
            self.gamestate.active_color = 0
        self.printBoard()