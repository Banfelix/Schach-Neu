
class Move:
    no_flags = 0b0000      
    en_passant_flag =  0b0001
    double_push_flag = 0b0010
    castling_flag =    0b0011

    rook_promotion_flag =   0b0100
    bishop_promotion_flag = 0b0101
    knight_promotion_flag = 0b0110
    queen_promotion_flag =  0b0111

    start_sq_mask = 0b0000000000111111
    end_sq_mask =   0b0000111111000000
    flag_mask =     0b1111000000000000

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


    def createPlayerMove(self, promotion_char=None):
        flag = self.flag_lookup.get(promotion_char)
        self.move_value = (flag << 12) | (self.end_sq << 6) | self.start_sq
        return self.move_value

    def createEngineMove(self, flag):
        self.move_value = (flag << 12) | (self.end_sq << 6) | self.start_sq
        return self.move_value