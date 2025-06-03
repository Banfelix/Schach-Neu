
def perft(board, depth):
    if depth == 0:
        return 1

    total_nodes = 0
    board.loadLegalMoves()
    moves = list(board.legal_moves)
    for move in moves:
        board.makeMove(move)
        total_nodes += perft(board, depth - 1)
        board.unMakeMove()
    return total_nodes
