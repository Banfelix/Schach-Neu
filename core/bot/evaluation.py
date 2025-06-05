from engine.piece import Piece
from bot.tables import piece_square_table
class Evaluation:
    def __init__(self):
        self.piece = Piece()
        self.max_value = 100000
        self.values = { self.piece.nopiece: 0,
                        self.piece.pawn: 100,
                        self.piece.knight: 300,
                        self.piece.bishop: 320,
                        self.piece.rook: 500,
                        self.piece.queen: 900,}

    def pieceCount(self, board):
        score = 0
        for piece, piecelist in board.piecelists.items():
            piece_type = self.piece.getPieceType(piece)
            if piece_type != self.piece.nopiece:
                for i in range(piecelist.num_pieces):
                    square = piecelist.occupied_squares[i]
                    table_score = piece_square_table[piece_type][square] if board.gamestate.active_color == 0 else piece_square_table[piece_type][63 - square]
                    if self.piece.getPieceColor(piece) == board.gamestate.active_color:
                        score += self.values.get(piece_type, 0)
                        score += table_score
                    else:
                        score -= self.values.get(piece_type, 0)
                        score -= table_score
                return score