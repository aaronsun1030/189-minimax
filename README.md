# 189 Minimax
Hi! This repo contains materials for the CS189 Project T. We hope that students can use this repo to learn all about minimax and how it can be applied to various topics.
## Learning Goals and How They Are Achieved
- Explore ideas necessary to implement minimax: game state spaces, game trees, heuristics, minimax procedure
  - Game states are game trees are discussed in the context of Chess and Tic Tac Toe with worked examples in the slides and notes
  - Minimax algorithm principles, pseudocode, and example of execution
- Understand how alpha-beta pruning and iterative deepening can be used to improve minimax in practice
  - We explain intuition of why we can prune, show worked examples for game trees, and pseudocode in the notes and slides
  - We describe the advantages of alpha-beta and iterative deepening for time and space complexity
- Implement these ideas to create competitive Chess AIs
  - We provide a Jupyter Notebook which walks students through using a heuristic and implementing the minimax algorithm
  - We have students extend these implementations by iterative deepening
  - We display graphs of runtime to show how alpha-beta pruning and iterative deepening improve upon minimax
- Explore extensions of these ideas such as quiescence search and move ordering
  - We provide a project where students implement quiescence search and move ordering on top of the earlier concepts
  - We show how these extensions allow a Chess AI to tackle challenging Chess puzzles
- Verify that students learned these concepts by asking conceptual and applied questions in a provided quiz
- By the end of this module, a student will be able to implement advanced game tree searching techniques and will understand the conceptual ideas and tradeoffs that come with these approaches

## Navigating the Repo
Our repo contains three main sections: teaching, assignments, and quiz.
- Teaching: contains both a note and slideshow which covers the material required for the assignments.
- Assignments: contains an introductory Jupyter Notebook that walks the student through basic minimax and pruning, as well as a more involved coding assignment.
- Quiz: contains a brief quiz that can be used to test a student's understanding.
