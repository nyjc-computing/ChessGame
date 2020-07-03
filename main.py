from chess import Board, King, Queen, Bishop, Knight, Rook, Pawn

game = Board()
# game.start()
# while game.winner is None:
#     game.display()
#     start, end = game.prompt()
#     game.update(start, end)
#     game.next_turn()
# print(f'Game over. {game.winner} player wins!')
game.add((0,1),Rook('black'))
game.add((0,2),King('white'))
game.display()
game.update((0,1),(0,2))
game.display()
game.winner