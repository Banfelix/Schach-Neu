

def bitboardToChessboard(bb):
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



        
bitboardToChessboard(1438234894565673)