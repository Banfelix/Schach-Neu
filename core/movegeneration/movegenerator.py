

class MoveGenerator:
    def __init__(self, board):
        self.allied_occupancies_bb = self.getAlliedOccupanciesBB(board)
        self.ennemy_occupancies_bb = self.getEnnemyOccupanciesBB(board)
        self.all_occupancies_bb = self.allied_occupancies_bb | self.ennemy_occupancies_bb

        self.second_row_mask = 0xFF00
        self.seventh_row_mask = 0x00FF000000000000


    def getAlliedOccupanciesBB(self, board):
        for piece, piecelist in board.piecelist.items():
            if board.piece.getPieceColor(piece)  == board.gamestate.active_color:
                for i in range(piecelist.num_pieces):
                    allied_occupancies_bb |= (1 << piecelist.occupied_squares[i])
        return allied_occupancies_bb
    
    def getEnnemyOccupanciesBB(self, board):
        for piece, piecelist in board.piecelist.items():
            if board.piece.getPieceColor(piece) != board.gamestate.active_color:
                for i in range(piecelist.num_pieces):
                    ennemy_occupancies_bb |= (1 << piecelist.occupied_squares[i])
        return ennemy_occupancies_bb