import time
import unittest
import TacticSolverSolution
import TacticSolver
import chess

solver = TacticSolverSolution.TacticSolver()
student = TacticSolver.TacticSolver()

class TestTactic(unittest.TestCase):

    def try_tactic(self, fen, depth, solution):
        def get_runtime(sol):
            current_depth = depth
            solver_move = False
            start = time.time()
            for m in solution:
                if solver_move:
                    assert sol.solve(board, current_depth, turn) == board.parse_san(m)
                    current_depth = max(current_depth - 2, 1)
                solver_move = not solver_move
                board.push_san(m)
            return time.time() - start
        board = chess.Board(fen)
        turn = -1 if board.turn else 1
        sample_time = get_runtime(solver)
        for m in solution:
            board.pop()
        student_time = get_runtime(student)
        print("Speedup over solution:", student_time / sample_time)

    def test_backrank(self):
        fen = "2kr4/1p1r1p2/2p1p2p/8/P1P1Rp2/8/1P3PPP/R5K1 w KQkq - 0 1"
        sol = ['Rxf4', 'Rd1+', 'Rxd1', 'Rxd1#']
        lowest_depth = 1
        self.try_tactic(fen, lowest_depth, sol)

    def test_skewer(self):
        fen = "8/8/r7/P4k2/3p1p2/3P4/5K2/7R b KQkq - 0 1"
        sol = ['Rxa5', 'Rh5+']
        lowest_depth = 1
        self.try_tactic(fen, lowest_depth, sol)
    
    def test_backrank_sack(self):
        fen = "3q4/6kp/2b1Q1p1/1p6/3r4/1B6/4RPPP/6K1 w KQkq - 0 1"
        sol = ['Qxc6',  'Rd1+', 'Bxd1', 'Qxd1+', 'Re1', 'Qxe1']
        lowest_depth = 2
        self.try_tactic(fen, lowest_depth, sol)

    def test_quick_mate(self):
        fen = "7k/8/5K2/8/8/8/8/6Q1 b - - 0 1"
        sol = ['Kh7', 'Qg7#']
        lowest_depth = 1
        self.try_tactic(fen, lowest_depth, sol)

    def test_promote_push(self):
        fen = "2B2k2/1p3p2/pn1P3p/4p1p1/8/5PP1/PP5P/6K1 b - - 0 1"
        sol = ['Nxc8', 'd7']
        lowest_depth = 1
        self.try_tactic(fen, lowest_depth, sol)
    
    def test_fork(self):
        fen = "8/8/5rk1/R4pp1/P1N5/2P3P1/1P3KP1/1r6 b - - 0 1"
        sol = ['Rc6', 'Ne5+']
        lowest_depth = 1
        self.try_tactic(fen, lowest_depth, sol)


if __name__ == '__main__':
    unittest.main()