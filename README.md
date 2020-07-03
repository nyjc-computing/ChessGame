# ChessGame

A repository for a chess game in Python (Assignment 12).



## Grading rubrics

See [grading.md](grading.md)



## Team Setup

1. Team leader is to fork the ChessGame repository (using the fork button) on Github. You now have a copy of the ChessGame repository under your account.
2. In the repository page, go to `Settings` → `Manage access` → `Invite a collaborator`. Add the rest of your team.
3. Each group member is to take one of the branches under **Core Requirements**.
4. **As a team**, discuss broadly how you will implement each feature.
5. Create any common attributes or methods that are required. You may wish to use the Github web editor for this.  
   **As a team**, standardise the name of these attributes or methods, and the method interfaces.  
   **Add docstrings** so that the whole team knows how to use these methods.  
   Commit your changes directly to the `master` branch.



## Instructions

1. In repl.it, each member should click on `new repl` → `Import from Github` and paste the URL of the repository.  
   This will create a repl that is linked to the repository, and is able to pull commits from and push commits to it.
2. In the repl, under the **Version Control** sidebar tab, create a new branch with the branch name.
3. Modify the code to implement your feature, making the minimum required modifications to the code. Code should be committed to the appropriate branch, not to `master` branch.
4. Test the code and make sure it is working.
5. Merge it back into the `main` branch by creating a pull request in Github.



## Core Requirements

★: Involves new attribute or minor edits to existing methods  
★★: Likely involves new method, plus edits  
★★★: Likely involves extensive edits  

The game code in `main.py` *should not be modified* (except for **moveerror** branch which will need to add keyword arguments when creating the game board).

### branch: **labels** (★)

Add row and column labels to make it easier for the player to count positions. These labels should appear when `display()` is called.

**Example:**  
```
  0 1 2 3 4 5 6 7
7 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
6 ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎ ♟︎
5                
4                
3                
2                
1 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
0 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
```

You may modify the code for `display()` as long as the displayed board remains identical.

### branch: **winner** (★)

Update the game so that it ends when a winner emerges.

If a player’s `King` piece is eliminated in any round, the opponent player wins.

### branch: **pawnfirstmove** (★)

In chess, the pawn may move two steps on *its first move*. Regardless of whether it took one or two steps on the first move, it may only move one step on subsequent moves.

### branch: **printmove** (★★)

Print the player's move after `prompt()`, before `next_turn()`

**Example:** `white pawn 01 -> 02`

### branch: **promotion** (★★)

Add additional code to check for **promotion** during `update()`. In chess, when a `Pawn` reaches the opposite side of the board, it may be promoted to a `Rook`, `Knight`, `Bishop`, or `Queen`.

For simplicity, you may assume that all promoted pawns will be promoted to `Queen` pieces.

The turn ends only after the piece is promoted.



## Bonus additions:

Teams may propose any other features as bonus additions if they are not mentioned here.

### branch: **check** (★★)

Print a message if any player is checked at the end of the turn.

**Example:** `white is checked!`

Check can be determined by taking the start position of each opponent piece on the board, taking the player’s King as the end position, and checking if this is a valid move for the opponent piece.

### branch: **debug** (★)

Add a `debug mode` to the game.

The game is in `debug mode` if the `Board` class is instantiated with the keyword argument `debug=True`.

In debug mode, the game output should display which step of the game it is at.

**Example:**
- `== DISPLAY ==` just before `display()` is called
- `== PROMPT ==` just before `prompt()` is called
- `== UPDATE ==` just before `update()` is called
- `== NEXT TURN ==` just before `next_turn()` is called

You may add more steps to print to demarcate different processes (e.g. checkmating, checking for game winner, ...)

### branch: **unchecking** (★)
(prerequisites: **checkmate**)

If a player is in checkmate, their next move must bring them out of checkmate, otherwise the move is invalid.

### branch: **moveerror** (★)

Define a custom `MoveError` to be raised if the move is an invalid move. This `MoveError` is to be raised when an invalid move is made.

`MoveError` should inherit from the parent class `Exception`. `Exception` is a built-in class provided in Python for creating custom error classes.

**Example:** `class MoveError(Exception):`

Any `MoveError`s raised should be handled with `try-except` and the player prompted until a valid move is made.

Other team members may inherit from this class to create custom errors, e.g. `StartPieceIsNotOwnError`, `EmptyPositionError`, `MovementBlockedError`, etc where necessary. This may make move validation easier.

### branch: **pawncapture** (★★)

Add additional move validation to the `Pawn` class for **capturing** moves.

A capturing move by a `Pawn` involves moving one step forward and one step to the left or right to capture another piece. A `Pawn` may only capture through such a capturing move, and never by moving only forward without a left or right step.

### branch: **moveclassifier** (★★)

Add a method that classifies and returns the type of move being made.

Possible options:
- `'move'` (a normal piece move)
- `'capture'` (when an opponent piece will be removed from end position)
- `'castling'`

The output from this may improve your code for the `update()` method, and for tasks such as **pawncapture** and **castling**

### branch: **nojump** (★★★)

In chess, pieces may not jump over another piece while moving to the end position. The Knight is the only piece that may do so.

Update the move validation code to check if there are any pieces in the path of movement.

### branch: **castling** (★★★)
(prerequisites: **pawnfirstmove**, **checkmate**)

Add additional move validation to the `King` and `Board` classes for **castling** moves.

Castling involves the `King` piece moving two steps towards one of the `Rook` pieces. The `Rook` piece then “jumps over” the `King` piece to be adjacent to it.

**Example:** `white king 40 -> 20 & white rook 00 -> 30` or `white king 40 -> 60 & white rook 70 -> 50`

Castling may only happen if:
- The `King` and `Pawn` pieces have never moved
- The player is not checkmated
- Castling will not cause the player to be checkmated
- There are no pieces between the `King` and `Rook`

### branch: **enpassant** (★★)
(prerequisites: **pawncapture**)

*En passant* is a special move in chess, introduced to account for the pawn’s ability to move two steps on its first move.

If a white pawn is on row 4 (or a black pawn on row 5), 

### branch: **movelog** (★)
(prerequisites: **printmove**)

As the game progresses, save each player’s move to a text file, `moves.txt`.

This file should be created at the start of the game if it does not exist.

**Example:**

```
white 01 -> 02
black 06 -> 05
...
```

