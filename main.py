from chess import Board, King, Rook, Pawn

def testGame():
    import os
    os.system('python3 -m unittest -v test_chess.TestCoreReqs')
    os.system('python3 -m unittest -v test_chess.TestBonusReqs')
testGame()

game = Board(debug=True)
game.start()
while game.winner is None:
    game.display()
    start, end = game.prompt()
    game.update(start, end)
    game.next_turn()
print(f'Game over. {game.winner} player wins!')
