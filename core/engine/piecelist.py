

class PieceList:                                                                                # Arbitrary maximum number of 16 of a certain type at once!
    def __init__(self, max_piece_count=16):                                                     # A PieceList Object exists for each piece in the Board object as a dict.: {int of the piece : PieceList Object}            
        self.occupied_squares = [0] * max_piece_count                                           # Holds the index of a square where a piece of the type exists              eg: [square Nr 8, square Nr 12, square Nr 3]
        self.map = [0] * 64                                                                     # For each square, tells where that squares piece is in occupied_squares    eg: map[8]=0 map[12]=1 map[3]=2
        self.num_pieces = 0

    def __len__(self):
        return self.num_pieces                                                                  # Returns how many of that piece there currently are

    def addPiece(self, square):
        self.occupied_squares[self.num_pieces] = square                                         # Sets the value next empty index in occupied_squares to the squares number     # The rest (After the index "self.num_pieces") of occupied_squres is garbage
        self.map[square] = self.num_pieces                                                      # Sets the index of map (the square-th entry) to the number of pieces, as this represents the index in occupied_squares
        self.num_pieces += 1                                                                    # Set the new amount of those pieces

    def removePiece(self, square):                                                              # To remove a piece
        piece_index = self.map[square]                                                          # Get the pieces index is in occupied_squares
        self.occupied_squares[piece_index] = self.occupied_squares[self.num_pieces - 1]         # Replace square on which there is not a pice anmyore with the current last entry thats not garbage
        self.map[self.occupied_squares[piece_index]] = piece_index                              # Update the map, as an occupied square has changed its index in occupied_squares
        self.num_pieces -= 1                                                                    # Update the amount of those pieces that are on the board, ie up to which index occupied_squares is not garbage

    def movePiece(self, start_square, target_square):                                           # To change the square on which a piece is 
        piece_index = self.map[start_square]                                                    # Get the pieces index is in occupied_squares 
        self.occupied_squares[piece_index] = target_square                                      # Replace the old square Nr with the new one in occupied_squares (no chabnge of index here)     
        self.map[target_square] = piece_index                                                   # Update the map. No need to clear 

    def __getitem__(self, index):                                                               # Returns the number of the occupied square of the given index eg.: square = whitepawn[0] calls __getitetm__(0) and return the first entry of occupied_squares # Will it be used?
        return self.occupied_squares[index]
