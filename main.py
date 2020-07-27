import curses
from chess import Interface, GameMaster, ChessBoard
from errors import InputError, MoveError

# def testGame():
#     import os
#     os.system('python3 -m unittest -v test_chess.TestCoreReqs')
#     os.system('python3 -m unittest -v test_chess.TestBonusReqs')
# testGame()


try:
    ui = Interface(height=19,
                   width=40,
                   )
    board = ChessBoard()

    game = GameMaster()
    game.start(board=board,
               ui=ui,
               )
    ui.set_msg('New game started.')
    while game.winner(board=board, ui=ui) is None:
        ui.set_board(board.as_str())
        while True:
            try:
                start, end, movetype = game.prompt(board=board,
                                                   ui=ui,
                                                   )
            except (InputError, MoveError) as e:
                ui.set_msg(e.msg)
            else:
                break
        ui.set_msg(game.format_move(start, end, movetype))
        game.update(start,
                    end,
                    movetype,
                    board=board,
                    )
        game.next_turn()
    ui.set_msg(f'Game over. {game.winner(board=board, ui=ui)} player wins!')
except Exception:
    ui.close()
    raise
