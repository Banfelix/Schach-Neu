def moveToAlgebraic(move_value):                                    # Used to print the legal moves as start -> end square for eg.: e1d1 
    start_sq_mask = 0b0000000000111111
    end_sq_mask   = 0b0000111111000000
    flag_mask     = 0b1111000000000000

    start_sq = move_value & start_sq_mask
    end_sq = (move_value & end_sq_mask) >> 6
    flag = (move_value & flag_mask) >> 12

    def squareToCoord(sq):
        file = sq % 8
        rank = sq // 8
        return chr(ord('a') + file) + str(rank + 1)

    promo_map = {
        0b0100: 'r',
        0b0101: 'b',
        0b0110: 'n',
        0b0111: 'q'
    }

    notation = squareToCoord(start_sq) + squareToCoord(end_sq)
    if flag in promo_map:
        notation += promo_map[flag]
    return notation
