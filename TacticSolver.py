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
        return self.find_move(board, depth, turn, -self.INFTY, self.INFTY)[1]

    def find_move(self, board, depth, turn, alpha, beta):
        """Does alpha-beta pruning to find the best move for the given position.
        If we hit depth 0, we run Quiescence search with double the depth."""
        # Hint: Put various ending conditions here

        # Hint: Put starting search values here

        # Hint: Search all possible moves here

        return best_value, best_refute

    def quiescence(self, board, depth, turn, alpha, beta):
        """Quiescence search, which searches checks and captures to a given depth.
        If the position is quiet, return the static score of the position."""
        # Hint: Put various ending conditions here

        # Hint: Put break condition on quiet positions here

        # Hint: Set starting search values here

        # Hint: Search valid non-quiet moves
        
        # Hint: If no moves are searched, return static score

        return best_value, best_refute  

    def move_order(self, board, killers, Q):
        """Yields the given moves for board, in the following order:
        1. Captures (MVV-LVA order)
        2. Checks
        The above two are given for quiescence Q, the below are not.
        3. Killers, or the best refutation for sister nodes
        4. All other legal moves in random order
        Note all possible moves are given if escaping check regardless of Q.
        """
        # Hint: Find captures and checks here
        
        # Hint: Sort captures here (use self.pieces)

        # Hint: Yield captures, checks, killers, remaining moves here