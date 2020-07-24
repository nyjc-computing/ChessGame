import os, unittest

from chess import Board, King, Queen, Bishop, Knight, Rook, Pawn

def gameSetupWithKings():
    game = Board(debug=True)
    game.add((4, 0), King('white'))
    game.add((4, 7), King('black'))
    return game

class TestIsValid(unittest.TestCase):
    def test_king_isvalid(self):
        '''King move validation'''
        testdata = {King('white'): [(4, 0), (4, 1), True],
                    King('white'): [(4, 0), (4, 2), False],
                    }
        for piece, (start, end, ans) in testdata.items():
            result = piece.isvalid(start, end)
            self.assertEqual(result, ans)

    def test_queen_isvalid(self):
        '''Queen move validation'''
        testdata = {Queen('white'): [(3, 0), (5, 2), True],
                    Queen('white'): [(3, 0), (5, 3), False],
                    }
        for piece, (start, end, ans) in testdata.items():
            result = piece.isvalid(start, end)
            self.assertEqual(result, ans)

    def test_bishop_isvalid(self):
        '''Bishop move validation'''
        testdata = {Bishop('white'): [(2, 0), (0, 2), True],
                Bishop('white'): [(2, 0), (1, 2), False],
                }
        for piece, (start, end, ans) in testdata.items():
            result = piece.isvalid(start, end)
            self.assertEqual(result, ans)

    def test_knight_isvalid(self):
        '''Knight move validation'''
        testdata = {Knight('white'): [(1, 0), (2, 2), True],
                    Knight('white'): [(1, 0), (1, 2), False],
                    }
        for piece, (start, end, ans) in testdata.items():
            result = piece.isvalid(start, end)
            self.assertEqual(result, ans)

    def test_rook_isvalid(self):
        '''Rook move validation'''
        testdata = {Rook('white'): [(0, 0), (0, 1), True],
                    Rook('white'): [(0, 0), (1, 1), False],
                    }
        for piece, (start, end, ans) in testdata.items():
            result = piece.isvalid(start, end)
            self.assertEqual(result, ans)

    def test_pawn_isvalid(self):
        '''Pawn move validation'''
        testdata = {Pawn('white'): [(0, 1), (0, 2), True],
                    Pawn('white'): [(0, 1), (1, 2), False],
                    }
        for piece, (start, end, ans) in testdata.items():
            result = piece.isvalid(start, end)
            self.assertEqual(result, ans)

class TestCoreReqs(unittest.TestCase):
    def test_winner(self):
        '''Identify game winner'''
        game = gameSetupWithKings()
        game.add((4, 5), Rook('white'))
        game.turn = 'white'
        game.update((4, 5), (4, 7))
        self.assertEqual(game.winner(), 'white')

        game = gameSetupWithKings()
        game.add((4, 2), Rook('black'))
        game.turn = 'black'
        game.update((4, 2), (4, 0))
        self.assertEqual(game.winner(), 'black')

    def test_pawn_first_move(self):
        '''Pawn can move two steps only on first move'''
        for col in range(7):
            game = gameSetupWithKings()
            game.add((col, 1), Pawn('white'))
            game.turn = 'white'
            self.assertTrue(game.valid_move((col, 1), (col, 3), game.turn))
            game.update((col, 1), (col, 3))
            self.assertEqual(game.get_piece((col, 3)).colour, 'white')
            self.assertIsNone(game.get_piece((col, 1)))
            self.assertFalse(game.valid_move((col, 3), (col, 5), game.turn))

            game = gameSetupWithKings()
            game.add((col, 6), Pawn('black'))
            game.turn = 'black'
            self.assertTrue(game.valid_move((col, 6), (col, 4), game.turn))
            game.update((col, 6), (col, 4))
            self.assertEqual(game.get_piece((col, 4)).colour, 'black')
            self.assertIsNone(game.get_piece((col, 6)))
            self.assertFalse(game.valid_move((col, 4), (col, 2), game.turn))

    def test_pawn_promotion(self):
        '''Pawn on last row is promoted'''
        for i in range(7):
            game = gameSetupWithKings()
            if i == 4:
                continue
            game.add((i, 6), Pawn('white'))
            game.turn = 'white'
            game.update((i, 6), (i, 7))
            self.assertEqual(game.get_piece((i, 7)).colour, 'white')
            self.assertEqual(game.get_piece((i, 7)).name, 'queen')

            game = gameSetupWithKings()
            game.add((i, 1), Pawn('black'))
            game.turn = 'white'
            game.update((i, 1), (i, 0))
            self.assertEqual(game.get_piece((i, 0)).colour, 'black')
            self.assertEqual(game.get_piece((i, 0)).name, 'queen')
    
    def test_quick_game(self):
        '''Row/col labels, player move, check message'''
        game = Board(debug=True)
        game.start()
        for start, end in [
                           ((4, 1), (4, 2)),
                           ((3, 6), (3, 5)),
                           ((3, 0), (7, 4)),
                           ((5, 6), (5, 5)), # check
                           ((7, 4), (4, 7)), # white win
                           ]:
            game.update(start, end)
            game.display()
            game.next_turn()

class TestBonusReqs(unittest.TestCase):
    def test_pawn_capture(self):
        '''Pawn captures diagonally'''
        game = gameSetupWithKings()
        game.add((0,3), Pawn('white'))
        game.add((1,4), Pawn('black'))
        game.turn = 'white'
        game.update((0, 3), (1, 4))
        self.assertEqual(game.get_piece((1, 4)).colour, 'white')
    
    def test_enpassant(self):
        '''Pawn can capture en passant'''
        game = gameSetupWithKings()
        game.add((3, 4), Pawn('white'))
        game.add((4, 6), Pawn('black'))
        game.turn = 'black'
        game.update((4, 6), (4, 4))
        game.next_turn()
        game.update((3, 4), (4, 5))
        self.assertEqual(game.get_piece((4, 5)).colour, 'white')
        self.assertIsNone(game.get_piece((4, 4)))

        game = gameSetupWithKings()
        game.add((3, 1), Pawn('white'))
        game.add((4, 3), Pawn('black'))
        game.turn = 'white'
        game.update((3, 1), (3, 3))
        game.next_turn()
        game.update((4, 3), (3, 2))
        self.assertEqual(game.get_piece((3, 2)).colour, 'black')
        self.assertIsNone(game.get_piece((3, 3)))

    def test_rook_castling(self):
        '''Rook can castle'''
        for colour, row in zip(['white', 'black'], [0, 7]):
            # TODO: make castling a King move
            game = gameSetupWithKings()
            game.add((0, row), Rook(colour))
            game.turn = colour
            game.update((4, row), (2, row))
            self.assertEqual(game.get_piece((3, row)).name, 'rook')
            self.assertEqual(game.get_piece((2, row)).name, 'king')

            game = gameSetupWithKings()
            game.add((7, row), Rook(colour))
            game.turn = colour
            game.update((4, row), (6, row))
            self.assertEqual(game.get_piece((5, row)).name, 'rook')
            self.assertEqual(game.get_piece((6, row)).name, 'king')

    def test_no_jump(self):
        '''Pieces cannot jump over pieces of same colour'''
        game = Board()
        game.add((4, 1), King('white'))
        game.add((4, 4), Rook('white'))
        game.add((4, 6), King('black'))
        game.add((4, 3), Rook('black'))
        game.turn = 'white'
        self.assertFalse(game.valid_move((4, 4), (4, 0), game.turn))
        self.assertFalse(game.valid_move((4, 3), (4, 7), game.turn))

    def test_next_move_uncheck(self):
        game = gameSetupWithKings()
        game.add((0, 1), Rook('black'))
        game.turn = 'black'
        game.update((0, 1), (0, 0))
        game.next_turn()
        # white king is in check, next move must bring it out of check
        self.assertFalse(game.valid_move((4, 0), (3, 0), game.turn))
        self.assertTrue(game.valid_move((4, 0), (4, 1), game.turn))

        game = gameSetupWithKings()
        game.add((0, 6), Rook('white'))
        game.turn = 'white'
        game.update((0, 6), (0, 7))
        game.next_turn()
        # black king is in check, next move must bring it out of check
        self.assertFalse(game.valid_move((4, 7), (3, 7), game.turn))
        self.assertTrue(game.valid_move((4, 7), (4, 6), game.turn))

    def test_move_logging(self):
        game = Board()
        game.start()
        game.update((4, 1), (4, 2))
        game.display()
        game.next_turn()
        if 'movelog.txt' in os.listdir():
            with open('movelog.txt', 'r') as f:
                line = f.readline()
                self.assertTrue('41' in line and '42' in line)