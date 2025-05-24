

def arbiterChecks(board):
        if not board.legal_moves:
            board.gamestate.running = False
            print("Checkmate!" if board.gamestate.inCheck else "Draw: Stalemate")
            return

        current_piece_count = pieceCount(board)

        if current_piece_count == board.piece_count and board.gamestate.pawns_bb == board.gamestate.previous_pawns_bb:
            board.gamestate.halfmoves += 1
        else:
            board.gamestate.halfmoves = 0

        if board.gamestate.pawns_bb != board.gamestate.previous_pawns_bb:
            board.gamestate.previous_pawns_bb = board.gamestate.pawns_bb

        if current_piece_count != board.piece_count:
            board.piece_count = current_piece_count

        if board.gamestate.halfmoves >= 50:
            board.gamestate.running = False
            print("Draw: 50-move rule")


def pieceCount(board):
        piece_count, bishop_count, knight_count = 0, 0, 0
        for square in board.board:
            piece = board.piece.getPieceType(square)
            if piece != board.piece.nopiece:
                piece_count += 1
                if piece == board.piece.knight: knight_count += 1
                if piece == board.piece.bishop: bishop_count += 1

        if piece_count == 2:
            board.gamestate.running = False
            print("Draw: Kings only")
        elif piece_count == 3 and (knight_count == 1 or bishop_count == 1):
            board.gamestate.running = False
            print("Draw: Insufficient material")

        return piece_count