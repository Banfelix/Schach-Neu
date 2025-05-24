
from movegeneration.precomputations.bishoplookup import bishop_moves_lookup
from movegeneration.precomputations.rooklookup import rook_moves_lookup
from movegeneration.precomputations.magics import rook_magics, rook_shifts, bishop_magics, bishop_shifts
from movegeneration.precomputations.movemasks import king_moves_mask, knight_moves_mask, rook_moves_mask, bishop_moves_mask, pawn_push_white_mask, pawn_capture_white_mask, pawn_push_black_mask, pawn_capture_black_mask
from movegeneration.precomputations.diagonalrays import diagonal_rays
from movegeneration.precomputations.orthogonalrays import orthogonal_rays
from movegeneration.precomputations.rays import rays
from engine.move import Move    
#from engine.piece import Piece

class MoveGenerator:
    def __init__(self, board):
        self.board = board
        self.ally_color = board.gamestate.active_color
        self.ennemy_color = board.gamestate.inactive_color
        self.all_pieces_piecelist = board.piecelists
        self.allied_piecelist = {k: v for k, v in board.piecelists.items() if board.piece.getPieceColor(k) == self.ally_color}
        self.ennemy_piecelist = {k: v for k, v in board.piecelists.items() if board.piece.getPieceColor(k) == self.ennemy_color}
        self.active_king_square = self.allied_piecelist[self.board.piece.king | self.ally_color][0]
        
        self.allied_occupancies_bb = 0
        self.ennemy_occupancies_bb = 0
        self.empty_squares_bb = 0
        self.all_occupancies_bb = 0
        self.all_occupancies_wo_ally_king_bb = 0
        self.pawns_bb = 0
        
        self.ennemy_attacks_bb = 0
        self.check_ray = 0
        self.checkers = []
        self.pinrays = []

        self.in_check = False
        self.in_double_check = False
        self.slider_check = False

        self.createOccupanciesBB()
        self.ennemyAttacks()
        self.getAllPinRays()
        
        if len(self.checkers)<=1:
            self.getHeavyPieceMoves()
            self.getPawnMoves()
            self.getKingMoves()
            if len(self.checkers) == 1: board.gamestate.inCheck = True
            else: board.gamestate.inCheck = False
        else:
            self.getKingMoves()
            board.gamestate.inCheck = True
        
        board.gamestate.pawns_bb = self.pawns_bb

        #print("Ammount of legal moves:" ,len(board.legal_moves))



    def createOccupanciesBB(self):
        for piece, piecelist in self.allied_piecelist.items():                                                          # Create occupancy bitboards for 
            is_allied_king = self.board.piece.getPieceType(piece) == self.board.piece.king 
            is_allied_pawn = self.board.piece.getPieceType(piece) == self.board.piece.pawn                              # Empty Square, Occupied Squares
            for i in range(piecelist.num_pieces):                                                                       # Allied Occupancies, Ennemy Occupancies
                square = piecelist[i]
                self.allied_occupancies_bb |= (1 << square)
                if not is_allied_king:
                    self.all_occupancies_wo_ally_king_bb |= (1 << square)
                if is_allied_pawn:
                    self.pawns_bb  |= (1 << square)

        for piece, piecelist in self.ennemy_piecelist.items():
            is_ennemy_pawn = self.board.piece.getPieceType(piece) == self.board.piece.pawn 
            for i in range(piecelist.num_pieces):
                square = piecelist[i]
                self.ennemy_occupancies_bb |= (1 << square)
                self.all_occupancies_wo_ally_king_bb |= (1 << square)
                if is_ennemy_pawn:
                    self.pawns_bb |= (1 << square)

        self.all_occupancies_bb = self.allied_occupancies_bb | self.ennemy_occupancies_bb
        self.empty_squares_bb = ~(self.all_occupancies_bb) & 0xFFFFFFFFFFFFFFFF


    def bitboardToMove(self, legal_moves_bb, start_square):
        while legal_moves_bb:
            lsb = legal_moves_bb & -legal_moves_bb                                                                   # Isolates the LSB
            target_square = lsb.bit_length() - 1                                                                     # Get "pos" of LSB (so the index)
            self.board.legal_moves.append(Move(start_square, target_square).createEngineMove(Move.no_flags))
            legal_moves_bb &= legal_moves_bb - 1                                                                     # clear the LSB, the loop restarts
   

    def getSliderBB(self, start_square, magics, shifts, move_mask, lookup_table):                                   # Returns bitboards for sliding piece movegeneration 
        relevant_occupancies = self.all_occupancies_bb & move_mask[start_square]                                    # With precalculated blocker setup from big lookup table
        magic_index = (relevant_occupancies * magics[start_square]) >> shifts[start_square]
        move_bb = lookup_table[start_square][magic_index] &~ self.allied_occupancies_bb     
        return move_bb          
                    

    def ennemyAttacks(self):
        king_bb = 1 << self.active_king_square

        for piece, piecelist in self.ennemy_piecelist.items():
            piece_type = self.board.piece.getPieceType(piece)

            for i in range(piecelist.num_pieces):
                square = piecelist[i]

                if piece_type == self.board.piece.bishop:
                    index = (self.all_occupancies_wo_ally_king_bb & bishop_moves_mask[square]) * bishop_magics[square] >> bishop_shifts[square]
                    attacks = bishop_moves_lookup[square][index]

                elif piece_type == self.board.piece.rook:
                    index = (self.all_occupancies_wo_ally_king_bb & rook_moves_mask[square]) * rook_magics[square] >> rook_shifts[square]
                    attacks = rook_moves_lookup[square][index]

                elif piece_type == self.board.piece.queen:
                    b_idx = (self.all_occupancies_wo_ally_king_bb & bishop_moves_mask[square]) * bishop_magics[square] >> bishop_shifts[square]
                    r_idx = (self.all_occupancies_wo_ally_king_bb & rook_moves_mask[square]) * rook_magics[square] >> rook_shifts[square]
                    attacks = bishop_moves_lookup[square][b_idx] | rook_moves_lookup[square][r_idx]

                elif piece_type == self.board.piece.knight:
                    attacks = knight_moves_mask[square]

                elif piece_type == self.board.piece.pawn:
                    attacks = pawn_capture_white_mask[square] if self.ennemy_color == self.board.piece.white else pawn_capture_black_mask[square]

                elif piece_type == self.board.piece.king:
                    attacks = king_moves_mask[square]

                else:
                    continue  # skip no pieces

                self.ennemy_attacks_bb |= attacks

                if attacks & king_bb:
                    self.checkers.append(square)

                    if piece_type in (self.board.piece.bishop, self.board.piece.rook, self.board.piece.queen):
                        self.slider_check = True
                        self.check_ray = rays[self.active_king_square][square]

        self.in_check = len(self.checkers) == 1
        self.in_double_check = len(self.checkers) == 2


    

    def getAllPinRays(self):
        for piece, piecelist in self.ennemy_piecelist.items():
            
            if not self.board.piece.isSlidingPiece(piece):
                continue  # Not a slider: skip

            for i in range(piecelist.num_pieces):
                pinner_square = piecelist.occupied_squares[i]                           # Square of a sliding piece
                rays_to_check = []

                if self.board.piece.isDiagonalSlider(piece):                # If a ray to the king exists, append it to potential pin rays
                    ray = diagonal_rays[self.active_king_square].get(pinner_square, 0)
                    if ray:
                        rays_to_check.append(ray)
                if self.board.piece.isOrthogonalSlider(piece):
                    ray = orthogonal_rays[self.active_king_square].get(pinner_square, 0)
                    if ray:
                        rays_to_check.append(ray)

                for ray in rays_to_check:                                                               # Check for pin condition: Exactly one allied piece in the ray
                    allied_blockers = ray & self.allied_occupancies_bb
                    enemy_blockers = (ray & self.ennemy_occupancies_bb) & ~(1 << pinner_square)
                    if allied_blockers.bit_count() == 1 and enemy_blockers == 0:
                        self.pinrays.append(ray)                                                        # Keep track of the pinrays


    def getPinRay(self, start_square):                              # Checks if a piece on start_square is pinned
        square = (1 << start_square)                                # If yes, returns the corresponding ray
        for i in range(len(self.pinrays)):                          # If no, returns false
            if square & self.pinrays[i] != 0:
                return self.pinrays[i]
        return False

    def getHeavyPieceMoves(self):   # Excludes King and pawn movegeneration
        for piece, piecelist in self.allied_piecelist.items():
            piece_type = self.board.piece.getPieceType(piece)

            for i in range(piecelist.num_pieces):
                start_square = piecelist.occupied_squares[i]

                if piece_type == self.board.piece.knight:                 # Knight moves
                    if self.getPinRay(start_square):
                        continue
                    move_bb = knight_moves_mask[start_square]
                    legal_moves_bb = move_bb & ~self.allied_occupancies_bb
                    if self.in_check:
                        legal_moves_bb &= (self.check_ray | (1 << self.checkers[0]))
                    self.bitboardToMove(legal_moves_bb, start_square)
                    continue

                legal_moves_bb = 0         # Slider moves                                                                         
                if self.board.piece.isOrthogonalSlider(piece):
                    legal_moves_bb |= self.getSliderBB(start_square, rook_magics, rook_shifts, rook_moves_mask, rook_moves_lookup)
                if self.board.piece.isDiagonalSlider(piece):
                    legal_moves_bb |= self.getSliderBB(start_square, bishop_magics, bishop_shifts, bishop_moves_mask, bishop_moves_lookup)

                if self.in_check:
                    legal_moves_bb &= (self.check_ray | (1 << self.checkers[0]))
                ray_mask = self.getPinRay(start_square)
                if ray_mask:
                    legal_moves_bb &= ray_mask
                self.bitboardToMove(legal_moves_bb, start_square)

    def getKingMoves(self):
        if self.ally_color == 0:  # white
            empty_kingside_mask = 0b1100000
            empty_queenside_mask = 0b1110
            kingside_rigths = self.board.gamestate.white_kingsidecastle_rights
            queenside_rigths = self.board.gamestate.white_queensidecastle_rights
        else:
            empty_kingside_mask = 0x6000000000000000
            empty_queenside_mask = 0xE00000000000000
            kingside_rigths = self.board.gamestate.black_kingsidecastle_rights
            queenside_rigths = self.board.gamestate.black_queensidecastle_rights
            
        for piece, piecelist in self.allied_piecelist.items():
            if self.board.piece.getPieceType(piece) == self.board.piece.king:
                for i in range(piecelist.num_pieces):
                    start_square = piecelist.occupied_squares[i]
                    legal_moves_bb = king_moves_mask[start_square]                                                                           
                    legal_moves_bb &= ~self.allied_occupancies_bb   
                    legal_moves_bb &= ~self.ennemy_attacks_bb                                                                   # Restrict the movement

                    self.bitboardToMove(legal_moves_bb, start_square)
                    if kingside_rigths:                                                                                         # Check if the neccessary squares are empty and not attacked
                        if (self.empty_squares_bb & empty_kingside_mask) == empty_kingside_mask:                                # If legal, create the castle move
                            if (not(self.ennemy_attacks_bb & empty_kingside_mask) and (not self.in_check)):
                                move_obj = Move(start_square, start_square + 2)  
                                encoded = move_obj.createEngineMove(Move.castling_flag)
                                self.board.legal_moves.append(encoded)

                    if queenside_rigths:
                        if (self.empty_squares_bb & empty_queenside_mask) == empty_queenside_mask:  
                            if (not(self.ennemy_attacks_bb & empty_queenside_mask) and (not self.in_check)): 
                                move_obj = Move(start_square, start_square - 2)  
                                encoded = move_obj.createEngineMove(Move.castling_flag)
                                self.board.legal_moves.append(encoded)


    def getPawnMoves(self):
        en_passant_bb = 1 << self.board.gamestate.enpassant_square if self.board.gamestate.enpassant_square is not None else 0
        color = self.board.gamestate.active_color
        direction = 8 if color == self.board.piece.white else -8
        promotion_rank = 7 if color == self.board.piece.white else 0
        start_rank_mask = 0xFF00 if color == self.board.piece.white else 0xFF000000000000

        for piece, piecelist in self.allied_piecelist.items():
            if self.board.piece.getPieceType(piece) != self.board.piece.pawn:
                continue
            for i in range(piecelist.num_pieces):
                start_square = piecelist.occupied_squares[i]

                if color == self.board.piece.white:                                                                                     # Check if the square in front is empty
                    single_push_bb = pawn_push_white_mask[start_square] & self.empty_squares_bb
                else:                                                                                                                   # If yes, add it to the legal moves bitboard
                    single_push_bb = pawn_push_black_mask[start_square] & self.empty_squares_bb
                legal_pushes = single_push_bb

                if legal_pushes and start_rank_mask & ( 1<< start_square):                                                              # If it can move one, and is on the starting rank
                    double_push_square_bb = (1 << (2 * direction + start_square))
                    if double_push_square_bb & self.empty_squares_bb:                                                                   # And the double push square is empty
                        legal_pushes |= double_push_square_bb

                if color == self.board.piece.white:                                                                                     # If a piece can be captured, or en passant
                    capture_bb = pawn_capture_white_mask[start_square] & (self.ennemy_occupancies_bb | en_passant_bb)
                else:
                    capture_bb = pawn_capture_black_mask[start_square] & (self.ennemy_occupancies_bb | en_passant_bb)
                legal_moves_bb = legal_pushes | capture_bb                                                                              # Add capture moves

                if self.in_check:                                                                                                       # Only moves that stop check from slider pieces
                    legal_moves_bb &= self.check_ray

                ray_mask = self.getPinRay(start_square)
                if ray_mask:
                    legal_moves_bb &= ray_mask
                
                if en_passant_bb != 0:                                                                                                      # Additional checks if there is an en passant move 
                    legality = self.en_passant_discovered_check(start_square , self.board.gamestate.enpassant_square, direction)
                    if legality == False:
                        legal_moves_bb &= ~(1 << self.board.gamestate.enpassant_square)
                    
                    legality = self.en_passant_check_evasion(start_square, self.board.gamestate.enpassant_square, direction)
                    if legality == True:
                        legal_moves_bb |= (1 << self.board.gamestate.enpassant_square)

                while legal_moves_bb:                                                                               # Handle promotions and special flags
                    lsb = legal_moves_bb & -legal_moves_bb
                    target_square = lsb.bit_length() - 1
                    target_rank = target_square // 8
                    move_obj = Move(start_square, target_square)

                    if target_rank == promotion_rank:
                        for promo_char in ['q', 'r', 'b', 'n']:
                            flag = move_obj.flag_lookup[promo_char]
                            encoded = move_obj.createEngineMove(flag)
                            self.board.legal_moves.append(encoded)
                    else:
                        if en_passant_bb & (1 << target_square):
                            flag = Move.en_passant_flag
                        elif abs(target_square - start_square) == 16:
                            flag = Move.double_push_flag
                        else:
                            flag = Move.no_flags
                        encoded = move_obj.createEngineMove(flag)
                        self.board.legal_moves.append(encoded)

                    legal_moves_bb &= legal_moves_bb - 1


    def en_passant_discovered_check(self, start_square, target_square, direction):
        en_passsant_capture_square = target_square - direction
        new_occupancy = self.all_occupancies_bb
        new_occupancy &= ~(1 << en_passsant_capture_square)             # Remove captured pawn
        new_occupancy &= ~(1 << start_square)                           # Remove moving pawn
        new_occupancy |= (1 << target_square)                           # Add moved pawn

        is_legal = True                                                                               # Test for discovered check (simulate ray between king and enemy sliders for the new pseudo position
        for piece, piecelist in self.ennemy_piecelist.items():
            piece_type = self.board.piece.getPieceType(piece)
            if piece_type not in (self.board.piece.rook, self.board.piece.queen):
                continue

            for j in range(piecelist.num_pieces):
                enemy_square = piecelist.occupied_squares[j]
                ray = rays[self.active_king_square].get(enemy_square, 0)

                if ray & (1 << (self.active_king_square + 1)) or  ray & (1 << (self.active_king_square - 1))!= 0:               # Check if it's a sliding attack and if the ray is empty after the capture
                    is_legal = False
                    return is_legal
                return is_legal
    

    def en_passant_check_evasion(self, start_square, target_square, direction):
        if self.checkers[0] == self.board.gamestate.enpassant_square - direction or (1 << self.board.gamestate.enpassant_square) & self.check_ray != 0:
            return True         # If a pawn is chekcing the king after adoublle push or an en passant capture would block a check ray returns true