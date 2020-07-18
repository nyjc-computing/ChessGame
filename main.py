from chess import Board, King, Queen, Bishop, Knight, Rook, Pawn

def testGame():
    import os
    os.system('python3 -m unittest -v test_chess.TestCoreReqs')
    os.system('python3 -m unittest -v test_chess.TestBonusReqs')
testGame()

game = Board(debug=True)
if game.debug:
    game.start()
    while game.winner is None:
        print('== DISPLAY ==')
        game.display()
        print('== PROMPT ==')
        start, end = game.prompt()
        print('== UPDATE ==')
        game.update(start, end)
        print('== NEXT TURN ==')
        game.next_turn()
else:
    game.start()
    while game.winner is None:
        game.display()
        start, end = game.prompt()
        game.update(start, end)
        game.next_turn()
print(f'Game over. {game.winner} player wins!')
