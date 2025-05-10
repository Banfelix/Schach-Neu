
class Move:
    no_flags = 0b0000      
    en_passant_flag =  0b0001
    double_push_flag = 0b0010
    castling_flag =    0b0011

    rook_promotion_flag =   0b0100
    bishop_promotion_flag = 0b0101
    knight_promotion_flag = 0b0110
    queen_promotion_flag =  0b0111

    start_sq_mask =  0b0000000000111111
    end_sq_mask =    0b0000111111000000
    flag_mask =      0b1111000000000000
    promotion_mask = 0b0100000000000000

    def __init__(self, start, end):
        self.move_value = None
        self.start_sq = start
        self.end_sq = end

        self.flag_lookup = {
            None: self.no_flags,
            'r': self.rook_promotion_flag,
            'b': self.bishop_promotion_flag,
            'n': self.knight_promotion_flag,
            'q': self.queen_promotion_flag}


    def createPlayerMove(self,board, promotion_char=None,):                             # A bit of extra logic for promotions
        flag = self.flag_lookup.get(promotion_char)
        self.move_value = (flag << 12) | (self.end_sq << 6) | self.start_sq
        self.move_value = self.legalityCheck(board)
        return self.move_value

    def createEngineMove(self, flag):                                                   # Flag setting is handled in movegeneration
        self.move_value = (flag << 12) | (self.end_sq << 6) | self.start_sq
        return self.move_value
    
    def legalityCheck(self, board):
        is_promotion = (self.move_value & self.promotion_mask) != 0                     # Check if promotion flag is set
        if is_promotion:                                                                # Compare full move (with flags) to legal moves
            if self.move_value in board.legal_moves:                                    # Promotion needs extra info for disambiguation, not just start and end square
                return self.move_value
            else:
                print("Illegal promotion move.")
                return None
        else:                                                                           # Mask out promotion / castling flags -> compare just move coords
            masked_move = self.move_value & ~(self.flag_mask)
            
            for legal_move in board.legal_moves:
                if (legal_move & ~(self.flag_mask)) == masked_move:
                    return legal_move                                                   # Return matching legal move in internal notation, with all correct flags
            print("Illegal move.")
            return None
