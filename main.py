from chess import Board, King, Queen, Bishop, Knight, Rook, Pawn

game = Board(debug=True)
game.start()
while game.winner is None:
    game.display()
    start, end = game.prompt()
    game.update(start, end)
    game.next_turn()
print(f'Game over. {game.winner} player wins!')

