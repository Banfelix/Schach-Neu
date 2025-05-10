
from movegeneration.precomputations.bishoplookup import bishop_moves_lookup
from movegeneration.precomputations.rooklookup import rook_moves_lookup
from movegeneration.precomputations.magics import rook_magics, rook_shifts, bishop_magics, bishop_shifts
from movegeneration.precomputations.movemasks import rook_moves_mask, bishop_moves_mask, pawn_push_white_mask, pawn_capture_white_mask, pawn_push_black_mask, pawn_capture_black_mask
from engine.move import Move    

class MoveGenerator:
    def __init__(self, board):
        self.allied_occupancies_bb = self.getAlliedOccupanciesBB(board)
        self.ennemy_occupancies_bb = self.getEnnemyOccupanciesBB(board)
        
        self.empty_squares_bb = self.getEmptySquaresBB()
        self.all_occupancies_bb = self.allied_occupancies_bb | self.ennemy_occupancies_bb
        self.ennemy_attacks_bb = 0

        self.first_row_mask = 0xFF
        self.second_row_mask = 0xFF00
        self.seventh_row_mask = 0x00FF000000000000
        self.eight_row_mask = 0xFF00000000000000
        self.a_row_mask = 0x0101010101010101
        self.h_row_mask = 0x1010101010101010

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
            legal_attacks_bb = move_bb
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
        en_passant_square_bb = 1 << board.gamestate.enpassant_square if board.gamestate.enpassant_square is not None else 0

        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceType(piece) == board.piece.pawn:
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]

                    if board.gamestate.active_color == 0:  # White
                        push_bb = pawn_push_white_mask[start_square] & self.empty_squares_bb
                        capture_bb = pawn_capture_white_mask[start_square] & (self.ennemy_occupancies_bb | en_passant_square_bb)
                        self.ennemy_attacks_bb |= pawn_capture_black_mask[start_square]
                        direction = 8    
                        promotion_rank  = 7
                    else:
                        push_bb = pawn_push_black_mask[start_square] & self.empty_squares_bb
                        capture_bb = pawn_capture_black_mask[start_square] & (self.ennemy_occupancies_bb | en_passant_square_bb)
                        self.ennemy_attacks_bb |= pawn_capture_white_mask[start_square]
                        direction = -8    
                        promotion_rank = 0

                    if board.gamestate.active_color == board.piece.getPieceColor(piece):
                        single_push_bb = 1 << (start_square + direction)
                        if not (self.empty_squares_bb & single_push_bb):
                            push_bb &= ~ (1 << (start_square + 2* direction))
                        legal_moves_bb = push_bb | capture_bb
                        while legal_moves_bb:
                            lsb = legal_moves_bb & -legal_moves_bb
                            target_square = lsb.bit_length() - 1
                            target_rank = target_square // 8
                            move_obj = Move(start_square, target_square)
                            if target_rank == promotion_rank:  
                                for promo_char in ['q', 'r', 'b', 'n']:
                                    encoded = move_obj.createEngineMove(move_obj.flag_lookup[promo_char])
                                    board.legal_moves.append(encoded)
                            else:
                                if en_passant_square_bb & (1 << target_square):
                                    encoded = move_obj.createEngineMove(Move.en_passant_flag)
                                elif abs(target_square - start_square) == 16:
                                    encoded = move_obj.createEngineMove(Move.double_push_flag)
                                else:
                                    encoded = move_obj.createEngineMove(Move.no_flags)
                                board.legal_moves.append(encoded)
                            legal_moves_bb &= legal_moves_bb - 1  
