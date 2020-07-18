# Rubric for grading

Grading will be carried out **based on the core requirements only**.

- Bonus additions, if implemented, should not break the game code or affect its core functionality.  
  Any breakage caused by additions will be penalised according to the rubrics.
- Each bonus addition, if successfully implemented by a member, gains the group one bonus mark.
- Further additions by the same member will not gain any bonus marks until other members of the group have also implemented bonus additions.


Teams may propose bonus additions

A score between 0-3 is given for each category. There are 5 categories in total:

- **Abstraction**  
  Assess how well the game is subdivided into methods and parts that are easy to understand.

- **Encapsulation**  
  Assesses whether data and methods are grouped appropriately, in ways that improve understanding of the code.

- **Clarity of code**  
  Assesses good programming practices in naming of variables and methods, and in writing code that is easy to understand.

- **User-friendliness**  
  Assesses whether the game provides useful information to players, whether for debugging or playing.

- **Functionality**  
  Assesses whether the game actually works.

**Max score:** 15

## Scoring system

### Abstraction

**0 marks** — Methods rely heavily on underlying implementation  
**1 mark** — Methods occasionally rely on underlying implementation  
**2 marks** — Methods have little reliance on underlying implementation, but could be better abstracted  
**3 marks** — Methods do not rely on underlying implementation and are appropriately abstracted

### Encapsulation
**0 marks** — Non-existent encapsulation  
**1 mark** — Game relies unnecessarily on variables and functions which are not part of the game or piece objects  
**2 marks** — Required variables and functions are encapsulated within the appropriate objects  
**3 marks** — Required variables and functions are encapsulated and appropriately defined (prudent use of `@staticmethod` and/or `@classmethod`)

### Clarity of code
**0 marks** — Attributes and methods have obtuse names; code is not possible to understand  
**1 mark** — Poor naming of attributes and methods; code is difficult to understand  
**2 marks** — Attributes and methods are appropriately named, and code is written with intuitive logic. Unnecessary commented code left behind.  
**3 marks** — Attributes and methods are appropriately named, methods have helpful docstrings, code is intuitive and easy to read.

### User-friendliness
**0 marks** — No useful output for debugging  
**1 mark** — Hard to tell what is wrong when testing the game; unhelpful console messages  
**2 marks** — Console messages indicate a problem and aid debugging somewhat  
**3 marks** — Console output is helpful for debugging and point to a clear, helpful cause

### Functionality
**0 marks** — Game does not run  
**1 mark** — Game is not able to run more than 2 turns  
**2 marks** — Game mostly works, but is unable to execute a chess game as expected  
**3 marks** — Game passes mosts tests, and failing tests does not affect core functionality
