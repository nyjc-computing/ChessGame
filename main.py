from chess import Board, King, Queen, Bishop, Knight, Rook, Pawn

game = Board()
game.start()
#print(game.get_coords('pawn','white'))
while game.winner is None:
    game.display()
    start, end = game.prompt()
    game.update(start, end)
    game.next_turn()
print(f'Game over. {game.winner} player wins!')
# game.display()
#game.add(King('white'),(0,0))
