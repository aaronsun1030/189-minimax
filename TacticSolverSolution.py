import sys
import random
import chess
from chess.polyglot import POLYGLOT_RANDOM_ARRAY, ZobristHasher

class TacticSolver:
    
    def __init__(self):
        """Create a new TacticSolver."""
        # A value which is better than winning.
        self.INFTY = sys.maxsize - 1
        # A value to indicate a player will win in the coming moves.
        self.WINNING_VALUE = sys.maxsize - 100
        # Lookup table for piece values
        self.pieces = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0}

    def static_score(self, board):
        """Returns the heuristic score of the board."""
        score = 0
        for color, value in [(chess.BLACK, -1), (chess.WHITE, 1)]:
            for piece in self.pieces:
                score += value * len(board.pieces(piece, color)) * self.pieces[piece]
        return score

    def solve(self, board, depth, turn):
        """Find the best move on board by searching at depth."""
        self.current_depth = depth
        return self.find_move(board, depth, turn, -self.INFTY, self.INFTY, None)[1]

    def find_move(self, board, depth, turn, alpha, beta, killer_moves):
        """Does alpha-beta pruning to find the best move for the given position.
        If we hit depth 0, we run Quiescence search with double the depth."""
        # Various ending conditions
        if board.is_checkmate():
            return -turn * (self.WINNING_VALUE - ((self.current_depth - depth))), None
        if board.can_claim_draw() or board.is_stalemate():
            return 0, None
        if depth == 0:
            return self.quiescence(board, self.current_depth * 2, 
                turn, -1 * self.INFTY, self.INFTY)

        # Starting search values
        best_value = -turn * self.INFTY
        best_refute, current_refute = None, None
        current_value = 0
        killers = set()

        # Search all possible moves
        for move in self.move_order(board, killer_moves, False):
            board.push(move)
            current_value, current_refute = self.find_move(board, depth - 1, 
                turn * -1, alpha, beta, killers)
            if current_refute:
                killers.add(current_refute)
            board.pop()
            if current_value * turn > best_value * turn:
                best_value = current_value
                best_refute = move
            if turn == 1:
                alpha = max(alpha, best_value)
            else:
                beta = min(beta, best_value) 
            if beta <= alpha:
                break

        return best_value, best_refute

    def quiescence(self, board, depth, turn, alpha, beta):
        """Quiescence search, which searches checks and captures to a given depth.
        If the position is quiet, return the static score of the position."""
        # Various ending conditions
        if board.is_checkmate():
            return -turn * (self.WINNING_VALUE - ((3 * self.current_depth - depth))), None
        if board.can_claim_draw() or board.is_stalemate():
            return 0, None
        if depth == 0:
            return self.static_score(board), None
        
        # Break condition on quiet positions
        pat = self.static_score(board)
        if not board.is_check():
            if turn == 1:
                alpha = max(pat, alpha)
                if pat >= beta:
                    return beta, None
            else:
                beta = min(pat, beta)
                if pat <= alpha:
                    return alpha, None

        # Starting search values
        best_value = -turn * self.INFTY
        best_refute = None
        current_value = 0

        # Search valid non-quiet moves
        for move in self.move_order(board, None, True):
            board.push(move)
            current_value, _ = self.quiescence(board, depth - 1, 
                turn * -1, alpha, beta)
            board.pop()
            if current_value * turn > best_value * turn:
                best_value = current_value
                best_refute = move
            if turn == 1:
                alpha = max(alpha, best_value)
            else:
                beta = min(beta, best_value) 
            if beta <= alpha:
                break
        
        # If no moves are searched
        if best_value == -turn * self.INFTY:
            return pat, None

        return best_value, best_refute  

    def move_order(self, board, killers, Q):
        """Outputs the given moves for board, in the following order:
        1. Captures
        2. Checks
        The above two are given for quiescence Q, the below are not.
        3. Killers, or the best refutation for sister nodes
        4. All other legal moves in random order
        """
        Q = Q and not board.is_check()
        moves = set(board.legal_moves)
        captures = []
        checks = []
        for m in moves:
            remove = False
            if board.is_capture(m):
                captures.append(m)
                remove = True
            elif board.gives_check(m):
                checks.append(m)
                remove = True
            if remove and killers:
                    killers.discard(m)
        captures.sort(key=lambda m: 90 if board.is_en_passant(m) else 
            9 * self.pieces[board.piece_type_at(m.from_square)] - 
            self.pieces[board.piece_type_at(m.to_square)])
        
        for c in captures:
            yield c
            moves.remove(c)
        for c in checks:
            yield c
            moves.remove(c)
        if not Q:
            if killers:
                for k in killers:
                    if k in moves:
                        yield k
                        moves.remove(k)
            for m in moves:
                yield m