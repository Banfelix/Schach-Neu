from engine.piece import Piece

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
        for piece in board.board:
            piece_type = self.piece.getPieceType(piece)
            if self.piece.getPieceColor(piece) == board.gamestate.active_color:
                score += self.values.get(piece_type, 0)
            else:
                score -= self.values.get(piece_type, 0)
        return score