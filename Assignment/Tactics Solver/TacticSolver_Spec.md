# Tactic Solver
## Introduction
Hope you all enjoyed the notebook! Now we can begin applying what we've learned to make an AI that efficiently solves chess **tactics**, or puzzles. In any tactic, there are a series of forcing moves which lead to an advantage for a given side. There will be some notable differences between what we implemented in the notebook and what you will be doing in your tactic solver AI. 

## 0. Heuristic
In the notebook, we used Stockfish as our heuristic to search with. However, Stockfish is too powerful for a basic tactic solver (it might be able to solve all the tactics before you even search). Hence, we will be using a basic material-based heuristic - each piece is worth a particular value, and the side with more pieces has a superior score. 

Note this has already been implemented for you in TacticSolver.py in the function static_score.

## 1. Move Ordering
In Alpha-Beta Pruning, since we prune more depending on whether we have already found a superior move, the order in which we consider our moves can affect runtime drastically. For instance, suppose we are considering 2 moves, move A and move B, which lead to +10 and -10, respectively. If we search move A first, we can easily prune move B in the first few iterations since move A is far better. However, if we search move B first, we would have to search through the continuations of move A completely to know move A is better. 

For that reason, we will implement a move ordering in our search. In chess, there are some general guidelines which we will follow in determining the ordering of our outputs. In particular, we will follow this ordering in considering our legal moves:

    1. Captures
        a. En passant (if possible). This is a special pawn capture which should be considered first.
        b. All other captures, based on the MVV-LVA (most valuable victim - least valuable aggressor) ordering. Using the valuations given in the heuristic, we will yield captures, sorting based on the most valuable victim first then sorting based on the least valuable aggressor for different captures of the same victim. To find the values of each piece, you can use the self.pieces instance variable which is a dictionary mapping from piece type to value.
    2. Checks, or any move that puts the opponent's king in check will be outputted in any order.
    3. Killers, explained in Section 2.
    4. All other legal moves in any order.
    
For Quiescence searches (Section 3), only the first 2 are yielded, unless the player is escaping check.

Your task is to implement this generator in the function move_order. In case you need a refresher what a generator is, see the [python wiki docs](https://wiki.python.org/moin/Generators). To identify each type of move, the [python-chess](https://python-chess.readthedocs.io/en/latest/) might prove useful. In addition, a list of useful functions is also provided at the end of this document.

## 2. Alpha-Beta Pruning (Basic)
This is just simple alpha-beta pruning which we covered extensively in the Jupyter notebook. However, unlike the notebook, we will NOT be implementing transposition tables, since they don't improve the runtime of a tactics solver very much. Make sure to account for the ending conditions of checkmate and draws, which you can identify using the [python-chess](https://python-chess.readthedocs.io/en/latest/) library. Once again, a list of useful functions is provided at the end of this document. Furthermore, we will have to implement the Killer Heuristic to work with our move ordering function.
    
### Killer Heuristic
The killer heuristic revolves around the idea that most moves result in a similar board state and will have similar appropriate replies from the opposing player. In other words, we want to remember the best response to each previous move, since the odds are it will be a good response to the current move as well. 

To do this, in find_move we return both the score of the current move and the best response move (refutation). Then, we must keep a record of all of these "killer moves" as we search legal moves, so we can use them to determine our move ordering for the potential responses for our current move.

Implement this in the find_move function. You can find more details on the killer heuristic on the [chessprogramming wiki](https://www.chessprogramming.org/Killer_Heuristic).

## 3. Quiescence Search
When we implemented this ourselves, we were having a very peculiar result, where our AI would make seemingly inexplicable moves, like sacrificing a queen for a pawn. This is because we didn't implement something called quiescenece search. When we search a position with a given depth, we fail to account for any moves following this depth, resulting in something called the ["horizon effect"](https://www.chessprogramming.org/Horizon_Effect) - we are unable to account for losses that occur past this depth limit. 

So when we sacrifice the queen for a pawn (say, at depth 1), our AI sees "hey, we won a pawn!" and then stops searching, which misses the crucial recapturing move where we lose our queen immediately after. To combat this, we will implement quiescence search, which does an additional, more limited search on captures/checks to ensure when we stop our search the position is "quiet" (less volatile).

At the end of the alpha-beta pruning, we will make an additional quiescence search of double the depth for our alpha-beta search, and the result of this will be our final output. Quiescence search has an additional break condition to reduce inefficient searches, called stand pat where we return the static position score if it falls outside our alpha-beta bounds before searching.

Implement this in the quiescence function. You can find the psuedocode for this function (specifically the stand pat section) on the [chessprogramming wiki](https://www.chessprogramming.org/Quiescence_Search). 

## Useful Functions
Here are some various useful functions and desciptions copied from the [python-chess](https://python-chess.readthedocs.io/en/latest/) library you might consider using in your solution:
    - Game End Conditions
        - chess.Board.is_checkmate(): Checks if the current position is a checkmate.
        - chess.Board.is_stalemate(): Checks if the current position is a stalemate.
        - chess.Board.can_claim_draw(): Checks if the player to move can claim a draw by the fifty-move rule or by threefold repetition.
    - Moves and Move Types
        - chess.Board.legal_moves: An iterator which returns legal moves in the current position.
        - chess.Board.is_capture(Move move): Checks if the given pseudo-legal move is a capture.
        - chess.Board.is_en_passant(Move move): Checks if the given pseudo-legal move is an en passant capture.
        - chess.Board.gives_check(Move move): Probes if the given move would put the opponent in check. The move must be at least pseudo-legal.
    - Other Board Properties
        - chess.Board.is_check(): Tests if the current side to move is in check.
        - chess.Board.piece_type_at(Square square): Gets the piece type at the given square.
        
## Testing
We have included some basic tactics in unittests.py. You should be able to solve them with the same depth as the solutions, as long as you have implemented quiescence search correctly. The comparison of the speed of your solution with the actual solutions is also given. Good luck!