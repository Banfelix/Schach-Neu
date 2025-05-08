

def bitboardToChessboard(bb):
    for rank in reversed(range(8)):  # print from rank 8 to 1
        row = ""
        for file in range(8):
            square_index = rank * 8 + file
            if (bb >> square_index) & 1:
                row += "x "
            else:
                row += "- "
        print(row)


        
bitboardToChessboard(1416240266379521)