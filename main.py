import curses
from chess import Board

# def testGame():
#     import os
#     os.system('python3 -m unittest -v test_chess.TestCoreReqs')
#     os.system('python3 -m unittest -v test_chess.TestBonusReqs')
# testGame()


screen = curses.initscr()
begin_y = 0; begin_x = 0
height = 10; width = 80
boardframe = curses.newwin(height, width, begin_y, begin_x)

begin_y = 11; begin_x = 0
height = 3; width = 80
statusbar = curses.newwin(height, width, begin_y, begin_x)

begin_y = 14; begin_x = 0
height = 1; width = 80
playerframe = curses.newwin(height, width, begin_y, begin_x)

screen.refresh()
# curses.endwin()

game = Board()
game.start()
try:
    while game.winner() is None:
        # breakpoint()
        boardframe.addstr(game.board())
        boardframe.refresh()
        
        playerframe.addstr('[TEXT] White player: ')
        playerframe.getstr(5)
        # start, end = game.prompt()
        game.update(start, end)
        game.next_turn()
except Exception as e:
    raise e
else:
    print(f'Game over. {game.winner()} player wins!')
finally:
    curses.endwin()

