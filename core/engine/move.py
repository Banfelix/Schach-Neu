
class Move:
    def __init__(self, start, end):
        self.move_value = None
        self.start_sq = start
        self.end_sq = end
        
        self.no_flags = 0b0000      
        self.en_passant_flag =  0b0001
        self.double_push_flag = 0b0010
        self.castling_flag =    0b0011

        self.rook_promotion_flag =   0b0100
        self.bishop_promotion_flag = 0b0101
        self.knight_promotion_flag = 0b0110
        self.queen_promotion_flag =  0b0111
        
        self.flag_lookup = {
            None: self.no_flags,
            'r': self.rook_promotion_flag,
            'b': self.bishop_promotion_flag,
            'n': self.knight_promotion_flag,
            'q': self.queen_promotion_flag}

        self.start_sq_mask = 0b0000000000111111
        self.end_sq_mask =   0b0000111111000000
        self.glam_mask =     0b1111000000000000

    def createPlayerMove(self, promotion_char=None):
        flag = self.flag_lookup.get(promotion_char)
        self.move_value = (flag << 12) | (self.end_sq << 6) | self.start_sq
        return self.move_value

    def createEngineMove(self, flag):
        self.move_value = (flag << 12) | (self.end_sq << 6) | self.start_sq
        return self.move_value