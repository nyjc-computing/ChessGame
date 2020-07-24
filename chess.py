from errors import *

class BasePiece:
    name = 'piece'
    def __init__(self, colour):
        if type(colour) != str:
            raise TypeError('colour argument must be str')
        elif colour.lower() not in {'white', 'black'}:
            raise ValueError('colour must be {white, black}')
        else:
            self.colour = colour
            self.moved = 0

    def __repr__(self):
        return f'BasePiece({repr(self.colour)})'

    def __str__(self):
        return f'{self.colour} {self.name}'

    def symbol(self):
        return f'{self.sym[self.colour]}'

    @staticmethod
    def vector(start, end):
        '''
        Return three values as a tuple:
        - x, the number of spaces moved horizontally,
        - y, the number of spaces moved vertically,
        - dist, the total number of spaces moved.
        
        positive integers indicate upward or rightward direction,
        negative integers indicate downward or leftward direction.
        dist is always positive.
        '''
        x = end[0] - start[0]
        y = end[1] - start[1]
        dist = abs(x) + abs(y)
        return x, y, dist


class King(BasePiece):
    name = 'king'
    sym = {'white': '♔', 'black': '♚'}
    def __repr__(self):
        return f"King('{self.colour}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        King can move one step in any direction
        horizontally, vertically, or diagonally.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 1) or (abs(x) == abs(y) == 1)

    
class Queen(BasePiece):
    name = 'queen'
    sym = {'white': '♕', 'black': '♛'}
    def __repr__(self):
        return f"Queen('{self.colour}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Queen can move any number of steps horizontally,
        vertically, or diagonally.
        '''
        x, y, dist = self.vector(start, end)
        return (abs(x) == abs(y) != 0) \
            or ((abs(x) == 0 and abs(y) != 0) \
            or (abs(y) == 0 and abs(x) != 0))


class Bishop(BasePiece):
    name = 'bishop'
    sym = {'white': '♗', 'black': '♝'}
    def __repr__(self):
        return f"Bishop('{self.colour}')"

    def isvalid(self, start: tuple, end: tuple):
        '''Bishop can move any number of steps diagonally.'''
        x, y, dist = self.vector(start, end)
        return (abs(x) == abs(y) != 0)


class Knight(BasePiece):
    name = 'knight'
    sym = {'white': '♘', 'black': '♞'}
    def __repr__(self):
        return f"Knight('{self.colour}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Knight moves 2 spaces in any direction, and
        1 space perpendicular to that direction, in an L-shape.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 3) and (abs(x) != 3 and abs(y) != 3)


class Rook(BasePiece):
    name = 'rook'
    sym = {'white': '♖', 'black': '♜'}
    def __repr__(self):
        return f"Rook('{self.colour}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Rook can move any number of steps horizontally
        or vertically.
        '''
        x, y, dist = self.vector(start, end)
        return (abs(x) == 0 and abs(y) != 0) \
            or (abs(y) == 0 and abs(x) != 0) 


class Pawn(BasePiece):
    name = 'pawn'
    sym = {'white': '♙', 'black': '♟︎'}
    def __repr__(self):
        return f"Pawn('{self.colour}')"

    def isvalid(self, start: tuple, end: tuple):
        '''Pawn can only move 1 step forward.'''
        x, y, dist = self.vector(start, end)
        if x == 0:
            if self.colour == 'black':
                if self.moved:
                    return (y == -1)
                else:
                    return (y == -2)
            elif self.colour == 'white':
                if self.moved:
                    return (y == 1)
                else:
                    return (y == 2)
        return False



class Board:
    '''
    The game board is represented as an 8×8 grid,
    with each position on the grid described as
    a pair of ints (range 0-7): col followed by row

    07  17  27  37  47  57  67  77
    06  16  26  36  46  56  66  76
    05  15  25  35  45  55  65  75
    04  14  24  34  44  54  64  74
    03  13  23  33  43  53  63  73
    02  12  22  32  42  52  62  72
    01  11  21  31  41  51  61  71
    00  10  20  30  40  50  60  70
    '''
    movetype = {'pawncapture', 'enpassant', 'castling', 'move'}
    def __init__(self, **kwargs):
        self.position = {}
        self.debug = kwargs.get('debug', False)

    def debugmsg(self, msg):
        if self.debug:
            print('[DEBUG]', msg)

    def coords(self, colour=None):
        '''
        Return list of piece coordinates.
        Filters for colour if provided in keyword argument.
        '''
        if colour in ('white', 'black'):
            return [coord for coord, piece in self.position.items() if piece.colour == colour]
        elif colour is None:
            return self.position.keys()
        else:
            raise ValueError('Invalid keyword argument colour={colour}')

    def pieces(self, colour=None):
        '''
        Return list of board pieces.
        Filters for colour if provided in keyword argument.
        '''
        if colour in ('white', 'black'):
            return [piece for piece in self.position.values() if piece.colour == colour]
        elif colour is None:
            return self.position.values()
        else:
            raise ValueError('Invalid keyword argument colour={colour}')
    
    def get_coords(self, colour, name):
        '''
        Returns a list of coords of pieces matching the name and
        colour.
        Returns empty list if none found.
        '''
        pieces = [i for i in self.coords() 
                  if self.get_piece(i).name == name
                  and self.get_piece(i).colour == colour
                  ]
        return pieces
    
    def get_piece(self, coord):
        '''
        Return the piece at coord.
        Returns None if no piece at coord.
        '''
        return self.position.get(coord, None)

    @staticmethod
    def coords_between(start, end):
        '''
        Return list of coordinates between start and end coord.
        List does not include start coord but includes end coord.
        Move must be horizontal, vertical, or diagonal only.
        '''
        x, y, dist = BasePiece.vector(start, end)
        if dist == 0:  # x == 0 and y == 0
            return []
        elif x == 0:  # vertical move
            incr = 1 if y > 0 else -1
            return [(start[0], row) for row in \
                    range(start[1] + incr, end[1], incr)]
        elif y == 0:  # horizontal move
            incr = 1 if x > 0 else -1
            return [(col, start[1]) for col in \
                    range(start[0] + incr, end[0], incr)]
        elif abs(x) == abs(y):
            y_incr = 1 if y > 0 else -1
            x_incr = 1 if x > 0 else -1
            cols = [(col, start[1]) for col in \
                    range(start[0] + y_incr, end[0] + y_incr, y_incr)]
            rows = [(start[0], row) for row in \
                    range(start[1] + x_incr, end[1] + x_incr, x_incr)]
            return [(col, row) for col, row in zip(cols, rows)]
        else:
            raise InvalidMoveError(start, end, 'Not a horizontal, vertical, or diagonal move')
        
    def add(self, coord, piece):
        '''Add a piece at coord.'''
        self.position[coord] = piece

    def remove(self, coord):
        '''
        Remove the piece at coord, if any.
        Does nothing if there is no piece at coord.
        '''
        if coord in self.coords():
            del self.position[coord]

    def move(self, start, end, **kwargs):
        '''
        Move the piece at start to end.
        Validation should be carried out first
        to ensure the move is valid.
        '''
        piece = self.get_piece(start)
        piece.moved += 1
        self.remove(start)
        self.add(end, piece)
        if kwargs.get('movetype') == 'castling':
            s_col, s_row = start
            e_col, e_row = end
            if e_col < s_col:    # castle leftward
                piece = self.get_piece((0, s_row))
                self.move((0, s_row), (3, e_row))
            elif e_col > s_col:  # castle rightward
                piece = self.get_piece((7, s_row))
                self.move((7, s_row), (5, e_row))
        elif kwargs.get('movetype') == 'enpassantcapture':
            s_col, s_row = start
            e_col, e_row = end
            enpassant_coord = (s_row, e_col)
            self.remove(enpassant_coord)

    def start(self):
        '''Set up the pieces and start the game.'''
        colour = 'black'
        self.add((0, 7), Rook(colour))
        self.add((1, 7), Knight(colour))
        self.add((2, 7), Bishop(colour))
        self.add((3, 7), Queen(colour))
        self.add((4, 7), King(colour))
        self.add((5, 7), Bishop(colour))
        self.add((6, 7), Knight(colour))
        self.add((7, 7), Rook(colour))
        for x in range(0, 8):
            self.add((x, 6), Pawn(colour))

        colour = 'white'
        self.add((0, 0), Rook(colour))
        self.add((1, 0), Knight(colour))
        self.add((2, 0), Bishop(colour))
        self.add((3, 0), Queen(colour))
        self.add((4, 0), King(colour))
        self.add((5, 0), Bishop(colour))
        self.add((6, 0), Knight(colour))
        self.add((7, 0), Rook(colour))
        for x in range(0, 8):
            self.add((x, 1), Pawn(colour))
        
        self.turn = 'white'
        
    def display(self):
        '''
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        '''
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order
        for row in range(7, -1, -1):
            for col in range(8):
                coord = (col, row)  # tuple
                if coord in self.coords():
                    piece = self.get_piece(coord)
                    print(f'{piece.symbol()}', end='')
                else:
                    piece = None
                    print(' ', end='')
                if col == 7:     # Put line break at the end
                    print('')
                else:            # Print a space between pieces
                    print(' ', end='')

    def prompt(self):
        '''
        Input format should be two ints,
        followed by a space,
        then another 2 ints
        e.g. 07 27
        '''
        def valid_format(inputstr):
            '''
            Ensure input is 5 characters: 2 numerals,
            followed by a space,
            followed by 2 numerals
            '''
            return len(inputstr) == 5 and inputstr[2] == ' ' \
                and inputstr[0:2].isdigit() \
                and inputstr[3:5].isdigit()
        
        def valid_num(inputstr):
            '''Ensure all inputted numerals are 0-7.'''
            for char in (inputstr[0:2] + inputstr[3:5]):
                if char not in '01234567':
                    return False
            return True
        
        def split_and_convert(inputstr):
            '''Convert 5-char inputstr into start and end tuples.'''
            start, end = inputstr.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            return (start, end)

        while True:
            inputstr = input(f'{self.turn.title()} player: ')
            if not valid_format(inputstr):
                print('Invalid input. Please enter your move in the '
                      'following format: __ __, _ represents a digit.')
            elif not valid_num(inputstr):
                print('Invalid input. Move digits should be 0-7.')
            else:
                start, end = split_and_convert(inputstr)
                if self.valid_move(start,
                                   end,
                                   self.turn,
                                   ):
                    return start, end

    def prompt_for_promotion_piece(self, coord):
        piece = self.get_piece(coord)
        upgrade_code = None
        while upgrade_code is not None and upgrade_code not in 'rkbq':
            upgrade_code = input('Select piece to promote pawn to '
                                 '(r=Rook, '
                                 'k=Knight, '
                                 'b=Bishop, '
                                 'q=Queen:'
                                  ).lower()
        classes = {'r': Rook,
                   'k': Knight,
                   'b': Bishop,
                   'q': Queen,
                   }
        return classes[upgrade_code]

    def check_and_promote(self, ReplacementPieceClass=Queen):
        for coord in self.get_coords('white', 'pawn'):
            col, row = coord
            if row == 7:
                if self.debug:
                    ReplacementPieceClass = Queen
                else:
                    ReplacementPieceClass = self.prompt_for_promotion_piece(coord)
                self.debugmsg(f'{self.get_piece(coord)} at {coord} promoted to {ReplacementPieceClass.name}.')
                self.remove(coord)
                self.add(coord, ReplacementPieceClass('white'))
        for coord in self.get_coords('black', 'pawn'):
            col, row = coord
            if row == 0:
                if self.debug:
                    ReplacementPieceClass = Queen
                else:
                    ReplacementPieceClass = self.prompt_for_promotion_piece(coord)
                self.debugmsg(f'{self.get_piece(coord)} at {coord} promoted to {ReplacementPieceClass.name}.')
                self.remove(coord)
                self.add(coord, ReplacementPieceClass('black'))

    def isblocked(self, start, end):
        piece = self.get_piece(start)
        if piece.name.lower() != 'knight':
            for coord in self.coords_between(start, end):
                if self.get_piece(coord) is not None:
                    return True
            return False
        else:
            return False

    def ispawncapture(self, start, end, colour):
        x, y, dist = BasePiece.vector(start, end)
        own_piece = self.get_piece(start)
        opp_piece = self.get_piece(end)
        if opp_piece is not None \
                and opp_piece.colour != self.turn \
                and abs(x) == 1:
            if own_piece.colour == 'white' and y == 1:
                return True
            elif own_piece.colour == 'black' and y == -1:
                return True
        else:
            return False
    
    def isenpassantcapture(self, start, end, colour):
        s_col, s_row = start
        e_col, e_row = end
        enpassant_coord = (s_row, e_col)
        own_piece = self.get_piece(start)
        opp_piece = self.get_piece(enpassant_coord)
        # TODO: Use more robust way of checking for 
        # enpassant capture
        if opp_piece is not None \
                and (self.turn == 'white' and s_row == 4
                     or self.turn == 'black' and s_row == 3) \
                and opp_piece.colour != self.turn \
                and opp_piece.moved == 1 \
                and abs(e_col - s_col) == 1:
            return True
        else:
            return False

    def iscastling(self, start, end, colour):
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if not start_piece.name == 'king' or start_piece.moved:
            return False
        x, y, dist = BasePiece.vector(start, end)
        if not (y == 0 and abs(x) == 2):
            return False
        rook_col = 0 if x < 0 else 7
        rook_row = 0 if colour == 'white' else 7
        rook_coord = (rook_col, rook_row)
        rook_piece = self.get_piece(rook_coord)
        if not rook_piece.name == 'rook' or rook_piece.moved:
            return False
        return True

    def valid_move(self, start, end, colour, **kwargs):
        try:
            movetype = self.classify_move(start, end, colour)
        except MoveError as e:
            if kwargs.get('debug', False):
                self.debugmsg(e.msg)
            return False
        else:
            if movetype is not None:
                return True
            else:
                return False

    def classify_move(self, start, end, colour):
        '''
        Checks for the following conditions:
        1. There is a start piece of the player's colour
        2. There is no end piece, or end piece is not of player's colour
        3. The move is a valid castling move
        4. There are no pieces between start and end coord (for Rook, Bishop, Queen)
        5. The move is valid for the selected piece
        6. The move is a valid pawn capture or en passant capture
        
        Returns the type of move, otherwise returns None
        '''
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        other_colour = 'white' if colour == 'black' else 'black'
        # (1)
        if start_piece is None or start_piece.colour != colour:
            raise InvalidPieceMovedError(start, end, f'{start_piece} does not belong to player')
        # (2)
        elif end_piece is not None and end_piece.colour == colour:
            raise DestinationIsBlockedError(start, end, f'Destination is occupied by {end_piece}')
        # (3)
        elif self.iscastling(start, end, colour):
            self.debugmsg(f'{start} -> {end} is castling move')
            return 'castling'
        # (4) 
        elif self.isblocked(start, end):
            raise PathIsBlockedError(start, end, f'path from {start} to {end} is blocked')
        # (5)
        elif start_piece.isvalid(start, end):
            self.debugmsg(f'{start} -> {end} is a valid {start_piece} move')
            return 'move'
        # (6)
        elif start_piece.name == 'pawn':
            if self.ispawncapture(start, end, colour):
                self.debugmsg(f'{start} -> {end} is a pawn capture')
                return 'pawncapture'
            elif self.isenpassantcapture(start, end, colour):
                self.debugmsg(f'{start} -> {end} is en passant capture')
                return 'enpassantcapture'
        else:
            raise InvalidMoveError(start, end, f'Invalid move for {start_piece}')

    def ischecked(self, colour):
        '''
        Return True if <colour> king is checked,
        else return False.
        '''
        for own_king_coord in self.get_coords(colour, 'king'):
            other_colour = 'white' if colour == 'black' else 'black'
            for opp_coord in self.coords(other_colour):
                if self.valid_move(opp_coord,
                                   own_king_coord,
                                   other_colour,
                                   debug = False,
                                   ):
                    self.debugmsg(f'{self.get_piece(own_king_coord)} is checked by {self.get_piece(opp_coord)}')
                    return True
        return False

    def update(self, start, end):
        '''Update board information with the player's move.'''
        self.remove(end)
        try:
            movetype = self.classify_move(start, end, self.turn)
        except MoveError:
            movetype = None
        self.move(start, end, movetype=movetype)
        self.check_and_promote()
        if self.ischecked(self.turn):
            print(f'{self.turn} is in check.')

    def next_turn(self):
        '''Hand the turn over to the other player.'''
        if self.turn == 'white':
            self.turn = 'black'
        elif self.turn == 'black':
            self.turn = 'white'

    def winner(self):
        white_king_alive = bool(self.get_coords('white', 'king'))
        black_king_alive = bool(self.get_coords('black', 'king'))
        if white_king_alive and black_king_alive:
            return None
        elif white_king_alive and not black_king_alive:
            return 'white'
        elif not white_king_alive and black_king_alive:
            return 'black'
        else:
            print('Neither king is on the board')