
                                                
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



        
bitboardToChessboard( 16212923956949443169)