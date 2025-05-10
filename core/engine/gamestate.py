

class GameState:
    def __init__(self):
        self.running = True              # To know when to end the programm
        self.halfmoves = 0               # One Fullmove is two halfmoves             # Gets updated during the game
        self.fullmoves = 0               # One Fullmove is white + black             # Gets updated during the game
        
        self.white_color = 0
        self.black_color = 8
        self.active_color = None                                # Gets updated during the game

        self.white_queensidecastle_rights = False               # Gets updated during the game only checks if pieces havent been moved
        self.white_kingsidecastle_rights = False                # Gets updated during the game only checks if pieces havent been moved
        self.black_queensidecastle_rights = False               # Gets updated during the game only checks if pieces havent been moved
        self.black_kingsidecastle_rights = False                # Gets updated during the game only checks if pieces havent been moved
    
        self.enpassant_square = None                            # Gets updated during the game after a double pawn push         # Needs to be None if there are none

