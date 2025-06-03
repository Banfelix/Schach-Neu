
class PieceList:                                                                                # Arbitrary maximum number of 16 of a certain type at once!
    def __init__(self, max_piece_count=16):                                             
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
    
    def __getitem__(self, index):
        return self.occupied_squares[index]
    