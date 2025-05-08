
from movegeneration.precomputations.bishoplookup import bishop_moves_lookup
from movegeneration.precomputations.rooklookup import rook_moves_lookup
from movegeneration.precomputations.magics import rook_magics, rook_shifts, bishop_magics, bishop_shifts
from movegeneration.precomputations.movemasks import rook_moves_mask, bishop_moves_mask
from engine.move import Move    

class MoveGenerator:
    def __init__(self, board):
        self.allied_occupancies_bb = self.getAlliedOccupanciesBB(board)
        self.ennemy_occupancies_bb = self.getEnnemyOccupanciesBB(board)
        
        self.empty_squares_bb = self.getEmptySquaresBB()
        self.all_occupancies_bb = self.allied_occupancies_bb | self.ennemy_occupancies_bb
        self.ennemy_attacks_bb = 0

        self.second_row_mask = 0xFF00
        self.seventh_row_mask = 0x00FF000000000000

        self.getRookMoves(board)
        self.getPawnMoves(board)
        self.getBishopMoves(board)

        print("Ennemy Attacks BB", self.ennemy_attacks_bb)

    def getAlliedOccupanciesBB(self, board):
        allied_occupancies_bb = 0
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceColor(piece)  == board.gamestate.active_color:
                for i in range(piecelist.num_pieces):
                    allied_occupancies_bb |= (1 << piecelist.occupied_squares[i])
        return allied_occupancies_bb
    
    def getEnnemyOccupanciesBB(self, board):
        ennemy_occupancies_bb = 0
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceColor(piece) != board.gamestate.active_color:
                for i in range(piecelist.num_pieces):
                    ennemy_occupancies_bb |= (1 << piecelist.occupied_squares[i])
        return ennemy_occupancies_bb
    
    def getEmptySquaresBB(self):
        emtpy_squares_bb = ~self.allied_occupancies_bb & ~self.ennemy_occupancies_bb
        return emtpy_squares_bb
    
    def getSliderBB(self, start_square, magics, shifts, move_mask, lookup_table):
        relevant_occupancies = self.all_occupancies_bb & move_mask[start_square]
        magic_index = (relevant_occupancies * magics[start_square]) >> shifts[start_square]
        move_bb = lookup_table[start_square].get(magic_index, 0)        
        return move_bb
    
    def bitboardToMove(self, legal_moves_bb, board, start_square):
        while legal_moves_bb:
            lsb = legal_moves_bb & -legal_moves_bb                                                                   # Isolates the LSB
            target_square = lsb.bit_length() - 1                                                                     # Get "pos" of LSB (so the index)
            board.legal_moves.append(Move(start_square, target_square).createEngineMove(Move.no_flags))
            legal_moves_bb &= legal_moves_bb - 1                                                                     # clear the LSB, the loop restarts

    def finaliser(self, board, piece, start_square, move_bb):
        if (board.piece.getPieceColor(piece) != board.gamestate.active_color):
            legal_attacks_bb = move_bb & ~self.ennemy_occupancies_bb
            self.ennemy_attacks_bb |= legal_attacks_bb
        else:
            legal_moves_bb = move_bb & ~self.allied_occupancies_bb
            self.bitboardToMove(legal_moves_bb, board, start_square)       

    ############################################################################################################################################
    def getRookMoves(self, board):
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceType(piece) == board.piece.rook:
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]
                    move_bb = self.getSliderBB(start_square, rook_magics, rook_shifts, rook_moves_mask, rook_moves_lookup)
                    self.finaliser(board, piece, start_square, move_bb)


    def getBishopMoves(self, board):
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceType(piece) == board.piece.bishop:
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]
                    move_bb = self.getSliderBB(start_square, bishop_magics, bishop_shifts, bishop_moves_mask, bishop_moves_lookup)
                    self.finaliser(board, piece, start_square, move_bb)


    def getPawnMoves(self, board):
        pawn_moves_bb = {}  # For bugfixing

        if board.gamestate.active_color == 0:  # White
            pawnlist = board.piecelists[board.piece.whitepawn]
            direction = 8
            left_capture_offset = 7
            right_capture_offset = 9
            starting_row_mask = self.second_row_mask
            promotion_rank = 7  # rank 8 (index 7)
            en_passant_row = 4
        else:  # Black
            pawnlist = board.piecelists[board.piece.blackpawn]
            direction = -8
            left_capture_offset = -9
            right_capture_offset = -7
            starting_row_mask = self.seventh_row_mask
            promotion_rank = 0  # rank 1 (index 0)
            en_passant_row = 3

        for i in range(pawnlist.num_pieces):
            square = pawnlist.occupied_squares[i]
            rank = square // 8
            file = square % 8
            move_mask = 0

            one_step = square + direction
            if 0 <= one_step < 64 and (self.empty_squares_bb & (1 << one_step)):
                move_mask |= (1 << one_step)
                two_step = square + 2 * direction
                if ((1 << square) & starting_row_mask) and (self.empty_squares_bb & (1 << two_step)):
                    move_mask |= (1 << two_step)

            if file > 0:
                left_diag = square + left_capture_offset
                if 0 <= left_diag < 64 and (self.ennemy_occupancies_bb & (1 << left_diag)):
                    move_mask |= (1 << left_diag)
                if board.gamestate.enpassant_square == left_diag and rank == en_passant_row:
                    move_mask |= (1 << left_diag)

            if file < 7:
                right_diag = square + right_capture_offset
                if 0 <= right_diag < 64 and (self.ennemy_occupancies_bb & (1 << right_diag)):
                    move_mask |= (1 << right_diag)
                if board.gamestate.enpassant_square == right_diag and rank == en_passant_row:
                    move_mask |= (1 << right_diag)

            if move_mask:
                pawn_moves_bb[square] = move_mask

                # For each target square in move mask
            while move_mask:
                lsb = move_mask & -move_mask
                target_square = lsb.bit_length() - 1
                target_rank = target_square // 8

                move_obj = Move(square, target_square)

                if target_rank == promotion_rank:
                    for promo_char in ['q', 'r', 'b', 'n']:
                        encoded_move = move_obj.createEngineMove(move_obj.flag_lookup[promo_char])
                        board.legal_moves.append(encoded_move)
                else:
                    if target_square == board.gamestate.enpassant_square and rank == en_passant_row:
                        encoded_move = move_obj.createEngineMove(Move.en_passant_flag)
                    elif abs(target_square - square) == 16:
                        encoded_move = move_obj.createEngineMove(Move.double_push_flag)
                    else:
                        encoded_move = move_obj.createEngineMove(Move.no_flags)

                    board.legal_moves.append(encoded_move)

                move_mask &= move_mask - 1  # clear the bit


