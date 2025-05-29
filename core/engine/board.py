from engine.piece import Piece
from engine.piecelist import PieceList
from engine.gamestate import GameState
from engine.move import Move
from helpers.fen import loadFEN
from movegeneration.movegenerator import MoveGenerator
from engine.arbiter import arbiterChecks
from debugs import moveToAlgebraic

class Board:
    def __init__(self):
        self.piece = Piece()
        self.gamestate = GameState()
        self.board = [self.piece.nopiece] * 64
        self.legal_moves = []
        self.piece_count = 0
        self.position_history = []
        self.move_history = []

        self.unicode_piece_map = {
            0: "·", 
            1: "♟", 2: "♞", 3: "♝", 4: "♜", 5: "♕", 6: "♚",
            9: "♙", 10: "♘", 11: "♗", 12: "♖", 13: "q", 14: "♔"}

        self.piecelists = {p: PieceList() for p in [
            self.piece.whitepawn, self.piece.whiteknight, self.piece.whitebishop,
            self.piece.whiterook, self.piece.whitequeen, self.piece.whiteking,
            self.piece.blackpawn, self.piece.blackknight, self.piece.blackbishop,
            self.piece.blackrook, self.piece.blackqueen, self.piece.blackking]}

        loadFEN(self)
        self.loadLegalMoves()
        self.printBoard()


    def loadLegalMoves(self):
        self.legal_moves.clear()
        MoveGenerator(self)

    def printBoard(self):
        transformed_moves = [moveToAlgebraic(move) for move in self.legal_moves],
        debug_info = [self.gamestate.fullmoves, self.gamestate.halfmoves, len(self.legal_moves), 
                    self.piecelists[5].occupied_squares, self.piecelists[1].occupied_squares, self.move_history,
                    self.board[35], self.gamestate.active_color]
        debug_info_name = ["fullmoves: ", "halfmoves: ", "number of legal moves: ", "White Queen Occupancies:","White pawn occupancies: ","Move history: ","Square number 35: ","Active Color:"]
        i = 0
        #print("Moves in the position:",transformed_moves)
        for rank in range(7, -1, -1):
            row = f"{rank + 1}    "
            for file in range(8):
                idx = rank * 8 + file
                piece = self.board[idx]
                symbol = symbol = self.unicode_piece_map.get(piece, "?")
                row += symbol + " "
            print(row, "    ",debug_info_name[i], debug_info[i])
            i += 1
        print("\n     a b c d e f g h")


    def setPiece(self, square, piece):
        old_piece = self.board[square]
        if old_piece != self.piece.nopiece:
            self.piecelists[old_piece].removePiece(square)

        self.board[square] = piece
        if piece != self.piece.nopiece:
            self.piecelists[piece].addPiece(square)
    
    def makeMove(self, move):
        start_square, end_square, flag = Move.moveDecode(move)
        moving_piece = self.board[start_square]
        captured_piece = self.board[end_square]

        self.move_history.append((start_square, end_square))
        self.position_history.append({
            #"legal_moves": list(self.legal_moves),
            "move": move,
            "moved_piece": moving_piece,
            "captured_piece": captured_piece,
            "active_color": self.gamestate.active_color,
            "inactive_color": self.gamestate.inactive_color,
            "enpassant_square": self.gamestate.enpassant_square,
            "castling_rights": (
                self.gamestate.white_kingsidecastle_rights,
                self.gamestate.white_queensidecastle_rights,
                self.gamestate.black_kingsidecastle_rights,
                self.gamestate.black_queensidecastle_rights),
            "halfmove_clock": self.gamestate.halfmoves,
            "fullmove_clock": self.gamestate.fullmoves,
            "running_game": self.gamestate.running})
        
        self.updateCastlingRights(moving_piece, start_square)

        if flag == Move.en_passant_flag:
            self.enPassantHandler(moving_piece, end_square)
        elif captured_piece != self.piece.nopiece:
            self.piecelists[captured_piece].removePiece(end_square)

        if flag == Move.double_push_flag:
            self.doublePushHandler(moving_piece, end_square)
        else:
            self.gamestate.enpassant_square = None

        if flag == Move.castling_flag:
            self.castleHandler(end_square)
            self.piecelists[moving_piece].movePiece(start_square, end_square)
            self.board[end_square] = moving_piece
            self.board[start_square] = self.piece.nopiece

        elif flag in {
            Move.rook_promotion_flag, Move.bishop_promotion_flag,
            Move.knight_promotion_flag, Move.queen_promotion_flag
        }:
            self.promotionHandler(moving_piece, start_square, end_square, flag)
        else:
            self.piecelists[moving_piece].movePiece(start_square, end_square)
            self.board[end_square] = moving_piece
            self.board[start_square] = self.piece.nopiece

        self.gamestate.active_color ^= self.gamestate.black_color
        self.gamestate.inactive_color ^= self.gamestate.black_color
        if self.gamestate.active_color == self.gamestate.black_color: self.gamestate.fullmoves += 1
        arbiterChecks(self)    
        self.loadLegalMoves()
        self.printBoard()
        self.verifyBoardState()

    def castleMoveRook(self, from_sq, to_sq):
        rook = self.board[from_sq]
        self.board[to_sq] = rook
        self.board[from_sq] = self.piece.nopiece
        self.piecelists[rook].movePiece(from_sq, to_sq)

    def enPassantHandler(self, moving_piece, end_square):
        offset = -8 if self.piece.getPieceColor(moving_piece) == self.piece.white else 8
        cap_sq = end_square + offset
        captured_piece = self.board[cap_sq]  # get captured pawn before removal
        self.board[cap_sq] = self.piece.nopiece
        self.piecelists[captured_piece].removePiece(cap_sq)

    def castleHandler(self, end_square):
        rook_moves = {6: (7, 5), 2: (0, 3), 62: (63, 61), 58: (56, 59)}
        if end_square in rook_moves:
            self.castleMoveRook(*rook_moves[end_square])

    def promotionHandler(self, moving_piece, start_square, end_square, flag):
        color = self.piece.getPieceColor(moving_piece)
        promo_map = {
            Move.rook_promotion_flag: self.piece.whiterook if color == 0 else self.piece.blackrook,
            Move.bishop_promotion_flag: self.piece.whitebishop if color == 0 else self.piece.blackbishop,
            Move.knight_promotion_flag: self.piece.whiteknight if color == 0 else self.piece.blackknight,
            Move.queen_promotion_flag: self.piece.whitequeen if color == 0 else self.piece.blackqueen
        }
        promoted = promo_map[flag]
        self.piecelists[moving_piece].removePiece(start_square)
        self.piecelists[promoted].addPiece(end_square)
        self.board[end_square] = promoted
        self.board[start_square] = self.piece.nopiece

    def doublePushHandler(self, moving_piece, end_square):
        direction = -8 if self.piece.getPieceColor(moving_piece) == self.piece.white else 8
        self.gamestate.enpassant_square = end_square + direction

    def updateCastlingRights(self, moving_piece, start_square):
        if moving_piece in [self.piece.whiterook, self.piece.blackrook]:
            if start_square == 0:
                self.gamestate.white_queensidecastle_rights = False
            elif start_square == 7:
                self.gamestate.white_kingsidecastle_rights = False
            elif start_square == 56:
                self.gamestate.black_queensidecastle_rights = False
            elif start_square == 63:
                self.gamestate.black_kingsidecastle_rights = False
        elif moving_piece in [self.piece.whiteking, self.piece.blackking]:
            if start_square == 4:
                self.gamestate.white_queensidecastle_rights = False
                self.gamestate.white_kingsidecastle_rights = False
            elif start_square == 60:
                self.gamestate.black_queensidecastle_rights = False
                self.gamestate.black_kingsidecastle_rights = False



    def unMakeMove(self):
        self.move_history.pop()
        print("UNDO MOVE CALLED")
        if not self.position_history:
            return

        last = self.position_history.pop() 
        move = last["move"]
        moved_piece = last["moved_piece"]
        captured_piece = last["captured_piece"]
        offset = -8 if last["active_color"] == self.gamestate.white_color else 8

        end_square, start_square, flag = Move.moveDecode(move)
        
        print("Remake move: ",start_square, "goes back to:", end_square)

            
        if flag == Move.castling_flag:
            if start_square == 6:
                rook_undo_moves = (5, 7)
            elif start_square == 2:
                rook_undo_moves = (3, 0)
            elif start_square == 62:
                rook_undo_moves = (61, 63)
            else: 
                rook_undo_moves = (59, 56)
            self.castleMoveRook(rook_undo_moves[0], rook_undo_moves[1])
        
        if flag == Move.queen_promotion_flag:
            promotion_piece = self.board[start_square]
            self.undoPromotionHandler(promotion_piece, moved_piece, start_square, end_square, captured_piece)
        
        elif flag == Move.rook_promotion_flag:
            promotion_piece = self.board[start_square]
            self.undoPromotionHandler(promotion_piece, moved_piece, start_square, end_square, captured_piece)        
        
        elif flag == Move.bishop_promotion_flag:
            promotion_piece = self.board[start_square]
            self.undoPromotionHandler(promotion_piece, moved_piece, start_square, end_square, captured_piece)
        
        elif flag == Move.knight_promotion_flag:
            promotion_piece = self.board[start_square]
            self.undoPromotionHandler(promotion_piece, moved_piece, start_square, end_square, captured_piece)
        
        elif flag == Move.en_passant_flag:
            captured_pawn = self.piece.blackpawn if last["active_color"] == self.gamestate.white_color else self.piece.whitepawn
            self.piecelists[moved_piece].movePiece(start_square, end_square)
            self.board[end_square] = moved_piece
            self.board[start_square] = captured_piece
            self.piecelists[captured_pawn].addPiece(start_square + offset)
            self.board[start_square + offset] = captured_pawn

        else:
            self.piecelists[moved_piece].movePiece(start_square, end_square)
            if captured_piece: self.piecelists[captured_piece].addPiece(start_square)
            self.board[end_square] = moved_piece
            self.board[start_square] = captured_piece

        self.gamestate.active_color = last["active_color"]
        self.gamestate.inactive_color = last["inactive_color"]
        self.gamestate.halfmoves = last["halfmove_clock"]
        self.gamestate.fullmoves = last["fullmove_clock"]
        self.gamestate.enpassant_square = last["enpassant_square"]
        self.gamestate.white_kingsidecastle_rights = last["castling_rights"][0]
        self.gamestate.white_queensidecastle_rights = last["castling_rights"][1]
        self.gamestate.black_kingsidecastle_rights = last["castling_rights"][2]
        self.gamestate.black_queensidecastle_rights = last["castling_rights"][3]
        self.gamestate.running = last["running_game"]
        #self.legal_moves = last["legal_moves"]
        self.loadLegalMoves()
        self.verifyBoardState()
        #print("active color before undo: ", last["active_color"])
        #print("WQ:", self.gamestate.white_queensidecastle_rights)
        #print("WK:", self.gamestate.white_kingsidecastle_rights)

    def undoPromotionHandler(self, promotion_piece, pawn ,start_square, end_square, captured_piece):
        self.piecelists[promotion_piece].removePiece(start_square)
        self.piecelists[pawn].addPiece(end_square)
        if captured_piece: self.piecelists[captured_piece].addPiece(start_square)
        self.board[start_square] = captured_piece
        self.board[end_square] = pawn

    def verifyBoardState(self):
        for square in self.piecelists[1].occupied_squares:
            if square != 0 and self.board[square] != 1:
                raise ValueError(f"Desync at square {square}")