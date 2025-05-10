
from movegeneration.precomputations.bishoplookup import bishop_moves_lookup
from movegeneration.precomputations.rooklookup import rook_moves_lookup
from movegeneration.precomputations.magics import rook_magics, rook_shifts, bishop_magics, bishop_shifts
from movegeneration.precomputations.movemasks import king_moves_mask, knight_moves_mask, rook_moves_mask, bishop_moves_mask, pawn_push_white_mask, pawn_capture_white_mask, pawn_push_black_mask, pawn_capture_black_mask
from engine.move import Move    

class MoveGenerator:
    def __init__(self, board):
        self.allied_occupancies_bb = self.getAlliedOccupanciesBB(board)
        self.ennemy_occupancies_bb = self.getEnnemyOccupanciesBB(board)
        
        self.empty_squares_bb = self.getEmptySquaresBB()
        self.all_occupancies_bb = self.allied_occupancies_bb | self.ennemy_occupancies_bb
        self.ennemy_attacks_bb = 0
        self.rook_squares = []


        self.getRookMoves(board)
        self.getPawnMoves(board)
        self.getBishopMoves(board)
        self.getQueenMoves(board)
        self.getKnightMoves(board)
        self.getKingMoves(board)

        print("Ennemy Attacks BB", self.ennemy_attacks_bb)

    def getAlliedOccupanciesBB(self, board):                                                                        # Returns a bitboard of all squares occupied by an ally piece
        allied_occupancies_bb = 0                                                                                   # By getting the square index and shifting a 1 to that position
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceColor(piece)  == board.gamestate.active_color:
                for i in range(piecelist.num_pieces):
                    allied_occupancies_bb |= (1 << piecelist.occupied_squares[i])
        return allied_occupancies_bb
    
    def getEnnemyOccupanciesBB(self, board):                                                                        # Returns a bitboard of all squares occupied by an ennemy piece in the same way
        ennemy_occupancies_bb = 0
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceColor(piece) != board.gamestate.active_color:
                for i in range(piecelist.num_pieces):
                    ennemy_occupancies_bb |= (1 << piecelist.occupied_squares[i])
        return ennemy_occupancies_bb
    
    def getEmptySquaresBB(self):                                                                                    # Returns a bitboard of all empty squares
        emtpy_squares_bb = ~self.allied_occupancies_bb & ~self.ennemy_occupancies_bb
        return emtpy_squares_bb
    
    def getSliderBB(self, start_square, magics, shifts, move_mask, lookup_table):                                   # Returns bitboards for sliding piece movegeneration 
        relevant_occupancies = self.all_occupancies_bb & move_mask[start_square]                                    # With precalculated blocker setup from big lookup table
        magic_index = (relevant_occupancies * magics[start_square]) >> shifts[start_square]
        move_bb = lookup_table[start_square].get(magic_index, 0)        
        return move_bb
    
    def bitboardToMove(self, legal_moves_bb, board, start_square):
        while legal_moves_bb:
            lsb = legal_moves_bb & -legal_moves_bb                                                                   # Isolates the LSB
            target_square = lsb.bit_length() - 1                                                                     # Get "pos" of LSB (so the index)
            board.legal_moves.append(Move(start_square, target_square).createEngineMove(Move.no_flags))
            legal_moves_bb &= legal_moves_bb - 1                                                                     # clear the LSB, the loop restarts

    def finaliser(self, board, piece, start_square, move_bb):                                                        # Creates the move in internal noation
        if (board.piece.getPieceColor(piece) != board.gamestate.active_color):
            legal_attacks_bb = move_bb
            self.ennemy_attacks_bb |= legal_attacks_bb                                                               # Updates the squares that ennemy pieces can attack -> for king movegen  
        else:
            legal_moves_bb = move_bb & ~self.allied_occupancies_bb
            self.bitboardToMove(legal_moves_bb, board, start_square)       

    ############################################################################################################################################

    def getRookMoves(self, board):
        for piece, piecelist in board.piecelists.items():   
            if board.piece.getPieceType(piece) == board.piece.rook:
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]                                                                            # Get the index of the sqaures with rooks
                    self.rook_squares.append(start_square)                                                                                  # Save them (for castling in king movegen)
                    move_bb = self.getSliderBB(start_square, rook_magics, rook_shifts, rook_moves_mask, rook_moves_lookup)                  # Get the bitboard of possible rook moves
                    self.finaliser(board, piece, start_square, move_bb)                                                                     # Creates the move


    def getBishopMoves(self, board):
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceType(piece) == board.piece.bishop:
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]                                                                            # Get the index of the sqaures with bishops
                    move_bb = self.getSliderBB(start_square, bishop_magics, bishop_shifts, bishop_moves_mask, bishop_moves_lookup)          # Get the bitboard of possible bishop moves
                    self.finaliser(board, piece, start_square, move_bb)                                                                     # Creates the move

    def getQueenMoves(self, board):
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceType(piece) == board.piece.queen:                                                                        # Still works in the same manner, but is handled as superposition of rook and bishop
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]
                    rook_moves_bb = self.getSliderBB(start_square, rook_magics, rook_shifts, rook_moves_mask, rook_moves_lookup)
                    bishop_moves_bb = self.getSliderBB(start_square, bishop_magics, bishop_shifts, bishop_moves_mask, bishop_moves_lookup)
                    move_bb = rook_moves_bb | bishop_moves_bb
                    self.finaliser(board, piece, start_square, move_bb)

    def getKnightMoves(self, board):                                                                                                        
        for piece, piecelist in board.piecelists.items():                                                               
            if board.piece.getPieceType(piece) == board.piece.knight:   
                for i in range(piecelist.num_pieces):                                                                                       # Get the bitboard of possible moves from a ceratain square and creates the move
                    start_square = piecelist.occupied_squares[i]
                    move_bb = knight_moves_mask[start_square]                                                                               # No special conditions for knight moves
                    self.finaliser(board, piece, start_square, move_bb)

    def getPawnMoves(self, board):
        en_passant_square_bb = 1 << board.gamestate.enpassant_square if board.gamestate.enpassant_square is not None else 0                 # Set a bitboard with the en passant square
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceType(piece) == board.piece.pawn:
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]

                    if board.gamestate.active_color == 0:                                                                                   # Set up cases for white and black movement
                        push_bb = pawn_push_white_mask[start_square] & self.empty_squares_bb
                        capture_bb = pawn_capture_white_mask[start_square] & (self.ennemy_occupancies_bb | en_passant_square_bb)
                        self.ennemy_attacks_bb |= pawn_capture_black_mask[start_square]                                                     # Updates ennemy attackers bitboard
                        direction = 8    
                        promotion_rank  = 7
                    else:
                        push_bb = pawn_push_black_mask[start_square] & self.empty_squares_bb
                        capture_bb = pawn_capture_black_mask[start_square] & (self.ennemy_occupancies_bb | en_passant_square_bb)
                        self.ennemy_attacks_bb |= pawn_capture_white_mask[start_square]
                        direction = -8    
                        promotion_rank = 0

                    if board.gamestate.active_color == board.piece.getPieceColor(piece):                                                    # To only create the moves of the color that's to move
                        single_push_bb = 1 << (start_square + direction)
                        if not (self.empty_squares_bb & single_push_bb):
                            push_bb &= ~ (1 << (start_square + 2* direction))                                                               # Handle single and double pushe legality
                        legal_moves_bb = push_bb | capture_bb
                        while legal_moves_bb:
                            lsb = legal_moves_bb & -legal_moves_bb
                            target_square = lsb.bit_length() - 1
                            target_rank = target_square // 8
                            move_obj = Move(start_square, target_square)
                            if target_rank == promotion_rank:                                                                               # If neccessary add promotion flag
                                for promo_char in ['q', 'r', 'b', 'n']:
                                    encoded = move_obj.createEngineMove(move_obj.flag_lookup[promo_char])
                                    board.legal_moves.append(encoded)
                            else:
                                if en_passant_square_bb & (1 << target_square):
                                    encoded = move_obj.createEngineMove(Move.en_passant_flag)                                               # Check for en passant and double pushes and add flags
                                elif abs(target_square - start_square) == 16:
                                    encoded = move_obj.createEngineMove(Move.double_push_flag)
                                else:
                                    encoded = move_obj.createEngineMove(Move.no_flags)
                                board.legal_moves.append(encoded)
                            legal_moves_bb &= legal_moves_bb - 1  

    def getKingMoves(self, board):
        for piece, piecelist in board.piecelists.items():
            if board.piece.getPieceType(piece) == board.piece.king:
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]
                    king_moves_bb = king_moves_mask[start_square] & ~self.allied_occupancies_bb & ~self.ennemy_attacks_bb
                    self.bitboardToMove(king_moves_bb, board, start_square)                                                     # Create the moves for non-castles
                    if board.gamestate.active_color == 0:  # white
                        empty_kingside_mask = 0b110
                        kingside_danger_squares_mask = 0b1110
                        empty_queenside_mask = 0b1110000
                        queenside_danger_squares_mask =0b1111000
                        kingside_rigths = board.gamestate.white_kingsidecastle_rights
                        queenside_rigths = board.gamestate.white_queensidecastle_rights
                    else:
                        empty_kingside_mask = 0x6000000000000000
                        kingside_danger_squares_mask = 0x7000000000000000 
                        empty_queenside_mask = 0x70000000000000
                        queenside_danger_squares_mask = 78000000000000
                        kingside_rigths = board.gamestate.white_kingsidecastle_rights
                        queenside_rigths = board.gamestate.white_queensidecastle_rights
                        
                    if kingside_rigths:                                                                                         # Check if the neccessary squares are empty and not attacked
                        if (self.empty_squares_bb & empty_kingside_mask) == empty_kingside_mask:                                # If legal, create the castle move
                            if not (self.ennemy_attacks_bb & kingside_danger_squares_mask):  
                                move_obj = Move(start_square, start_square + 2)  
                                encoded = move_obj.createEngineMove(Move.castling_flag)
                                board.legal_moves.append(encoded)
                    if queenside_rigths:
                        if (self.empty_squares_bb & empty_queenside_mask) == empty_queenside_mask:  
                            if not (self.ennemy_attacks_bb & queenside_danger_squares_mask):  
                                move_obj = Move(start_square, start_square - 2)  
                                encoded = move_obj.createEngineMove(Move.castling_flag)
                                board.legal_moves.append(encoded)
