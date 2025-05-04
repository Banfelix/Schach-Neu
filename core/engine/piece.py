

class Piece:
    def __init__(self):
        self.nopiece = 0
        self.pawn = 1          
        self.knight = 2         
        self.bishop = 3         
        self.rook = 4           
        self.queen = 5          
        self.king = 6           

        self.white = 0                                  # The 4th Bit is a Flag for the color
        self.black = 8          

        self.whitepawn = self.pawn | self.white         #1
        self.whiteknight = self.knight | self.white     #2
        self.whitebishop = self.bishop | self.white     #3
        self.whiterook = self.rook | self.white         #4
        self.whitequeen = self.queen | self.white       #5
        self.whiteking = self.king | self.white         #6

        self.blackpawn = self.pawn | self.black         #9
        self.blackknight = self.knight | self.black     #10
        self.blackbishop = self.bishop | self.black     #11
        self.blackrook = self.rook | self.black         #12
        self.blackqueen = self.queen | self.black       #13
        self.blackking = self.king | self.black         #14

        self.pieces = [self.whitepawn, self.whiteknight, self.whitebishop, self.whiterook, self.whitequeen, self.whiteking,
                       self.blackpawn, self.blackknight, self.blackbishop, self.blackrook, self.blackqueen, self.blackking]
        
        self.typemask = 0b0111
        self.colormask = 0b1000
    
    def getPieceType(self, piece):                                          # Returns the integer corresponding to the piece type
        return piece & self.typemask

    def getPieceColor(self, piece):                                         # Returns the integer corresponding to the piece color
        return piece & self.colormask

    def pieceToSymbol(self, piece):                                         # Returns the symbol of the piece
        type = self.getPieceType(piece)
        color = self.getPieceColor(piece)
 
        if type == 1: symbol = "p" 
        elif type == 2: symbol = "n"
        elif type == 3: symbol = "b"
        elif type == 4: symbol = "r"
        elif type == 5: symbol = "q"
        elif type == 6: symbol = "k"
        else: return "--"
        if not color: symbol = symbol.upper()
        return symbol

    def symbolToPiece(self, symbol):                                        # Returns the intger of the piece corresponding to the given symbol
        if symbol == "--": return 0
        
        color = self.white if symbol.isupper() else self.black
        symbol = symbol.lower()
        
        if symbol == "p": type = self.pawn
        elif symbol == "n": type = self.knight
        elif symbol == "b": type = self.bishop
        elif symbol == "r": type = self.rook
        elif symbol == "q": type = self.queen
        elif symbol == "k": type = self.king
        else: return None
        return type | color

