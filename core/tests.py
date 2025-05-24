

                  
def bitboardToChessboard(bb):                                   # Helper stuff, prints out a the bitboard corresponding to an integer, for ease of visualisation
    for rank in range(7, -1, -1):  # rank 8 to 1
        row = f"{rank + 1}    "    # row label
        for file in range(8):
            square_index = rank * 8 + file
            if (bb >> square_index) & 1:
                row += "x "
            else:
                row += "- "
        print(row)
    print("\n     a b c d e f g h")



        
bitboardToChessboard(1090921693184)

'''
def generate_rook_moves_mask():
    rook_masks = []
    for sq in range(64):
        mask = 0
        rank = sq // 8
        file = sq % 8

        # Up
        for r in range(rank + 1, 8):
            mask |= 1 << (r * 8 + file)

        # Down
        for r in range(rank - 1, -1, -1):
            mask |= 1 << (r * 8 + file)

        # Right
        for f in range(file + 1, 8):
            mask |= 1 << (rank * 8 + f)

        # Left
        for f in range(file - 1, -1, -1):
            mask |= 1 << (rank * 8 + f)

        rook_masks.append(mask)
    return rook_masks

print(generate_rook_moves_mask())
'''