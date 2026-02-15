# Sudoku

## Overview

A python-based Sudoku game with a custom **Recursive Backtracking Solver** and a heuristic-based **Hint Egine**.

## Demo

[My Demo on YouTube](https://www.youtube.com/watch?v=WoQNfTKX4tA)

## Core Logic

### Backtracking Solver
- Uses recursive depth-first search to fill the board.
- Validates row, column, and 3×3 block constraints.
- Stores the generated solution at board load to enable validation and hint features.

### Legals Management
- Automatically computes legal values for each empty cell.
- Updates candidates dynamically when values change.
- Supports a manual candidate mode for user-edited possibilities.

### Hint System
- Detects cells with a single valid value (singletons).
- Can visually highlight hints or apply them directly.
- Includes an autoplay mode that repeatedly fills singleton cells.

## Technologies and Architecture
- Language: Python
- Graphics: cmu_graphics (Proprietary framework for CMU 15-112)
- Design Pattern: Modular architecture separating screen routing (Main.py), UI/Difficulty selection (LevelSelector.py), and core engine logic (Sudoku.py).

## Note on Running the App
This project requires the `cmu_graphics` library provided by Carnegie Mellon University. As this is a proprietary framework, the source code is provided primarily for logic review. Please refer to the Demo Video to see the application in action.