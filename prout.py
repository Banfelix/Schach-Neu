class PieceList:                                                                                # Arbitrary maximum number of 16 of a certain type at once!
    def __init__(self, max_piece_count=17):                                             
        self.occupied_squares = [0] * max_piece_count                                      
        self.map = [0] * 64                                                                
        self.num_pieces = 0

    def __len__(self):
        return self.num_pieces                                                             

    def addPiece(self, square):
        self.occupied_squares[self.num_pieces] = square                                    
        self.map[square] = self.num_pieces                                                 
        self.num_pieces += 1                                                               
        
    def removePiece(self, square):                                                         
        piece_index = self.map[square]                                                     
        self.occupied_squares[piece_index] = self.occupied_squares[self.num_pieces - 1]    
        self.map[self.occupied_squares[self.num_pieces - 1]] = piece_index
        self.occupied_squares[self.num_pieces-1] = 0 
        self.map[square] = 0
        self.num_pieces -= 1                                                               

    def movePiece(self, start_square, target_square):                                      
        piece_index = self.map[start_square]                                               
        self.occupied_squares[piece_index] = target_square                          
        self.map[target_square] = piece_index           
        self.map[start_square] = 0


indices = []
for j in range(6):
    for i in range(10):
        indices.append(i)


piecelist = PieceList()

piecelist.addPiece(49)
piecelist.addPiece(42)
piecelist.addPiece(30)
print("After add 49, 42, 30")
print(piecelist.occupied_squares)
print(piecelist.map)
print(indices, "\n")


piecelist.movePiece(42, 50)
print("After move from 42 to 50")
print(piecelist.occupied_squares)
print(piecelist.map)
print(indices, "\n")

piecelist.addPiece(42)
print("After add 42")
print(piecelist.occupied_squares)
print(piecelist.map)
print(indices, "\n")

piecelist.removePiece(30)
print("After remove 30")
print(piecelist.occupied_squares)
print(piecelist.map)
print(indices, "\n")
