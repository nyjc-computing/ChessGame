import curses
from errors import *


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

def debugmsg(msg):
    print('[DEBUG]', msg)



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
        x, y, dist = vector(start, end)
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
        x, y, dist = vector(start, end)
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
        x, y, dist = vector(start, end)
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
        x, y, dist = vector(start, end)
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
        x, y, dist = vector(start, end)
        return (abs(x) == 0 and abs(y) != 0) \
            or (abs(y) == 0 and abs(x) != 0) 


class Pawn(BasePiece):
    name = 'pawn'
    sym = {'white': '♙', 'black': '♟︎'}
    def __repr__(self):
        return f"Pawn('{self.colour}')"

    def isvalid(self, start: tuple, end: tuple):
        '''Pawn can only move 1 step forward.'''
        x, y, dist = vector(start, end)
        if x == 0:
            if self.colour == 'black':
                if self.moved:
                    return (y == -1)
                else:
                    return (0 > y >= -2)
            elif self.colour == 'white':
                if self.moved:
                    return (y == 1)
                else:
                    return (0 < y <= 2)
        return False



class Interface:
    '''
    The Interface is responsible for:

    1. Displaying the welcome screen
    2. Displaying the board
    3. Displaying the player prompt
    4. Displaying any messages
    '''
    def __init__(self, **kwargs):
        self.height = kwargs.get('height', 20)
        self.width = kwargs.get('width', 20)
        self.screen = curses.initscr()
        y_pos = 0
        this_height = self.height - 8
        self.board = curses.newwin(this_height, self.width, y_pos, 0)
        self.board.border()
        self.board.addstr(0, 2, 'Board')

        y_pos += this_height
        this_height = 5
        self.msgbar = curses.newwin(this_height, self.width, y_pos, 0)
        self.msgbar.border()
        self.msgbar.addstr(0, 2, 'Messages')

        y_pos += this_height
        this_height = 3
        self.inputbar = curses.newwin(this_height, self.width, y_pos, 0)
        self.inputbar.border()
        self.inputbar.addstr(0, 2, 'Player')

    def set(self, strlist, target):
        if type(strlist) == str:
            strlist = strlist.split('\n')
        if type(strlist) == list:
            for row, line in enumerate(strlist, 1):
                target.addstr(row, 1, line)
        target.refresh()

    def set_board(self, strlist):
        self.set(strlist, self.board)

    def set_msg(self, strlist):
        self.set(strlist, self.msgbar)
    
    def get_player_input(self, msg):
        self.set(msg, self.inputbar)
        value = self.inputbar.getstr(5).decode('utf-8') 
        self.set((self.width - 2)*' ', self.inputbar)
        return value

    def refresh(self):
        self.screen.refresh()
    
    def close(self):
        curses.endwin()



class GameMaster:
    '''
    The GameMaster is responsible for:

    1. Prompting the player for a move
    2. Checking if the move is valid
       (and re-prompting the player)
    3. Passing the move to the board for updating
    4. Checking if a player has won,
       and checking game status
    '''
    def __init__(self, **kwargs):
        pass

    @staticmethod
    def format_move(start, end, movetype):
        return (f'{start} -> {end} {movetype}')

    def start(self, **kwargs):
        kwargs['board'].start()
        kwargs['ui'].refresh()
        self.turn = 'white'
    
    def prompt(self, **kwargs):
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

        inputstr = kwargs['ui'].get_player_input(f'{self.turn.title()} player: ')
        if not valid_format(inputstr):
            raise InputError('Invalid input. Please enter your move in the following format: __ __, _ represents a digit.')
        elif not valid_num(inputstr):
            raise InputError('Invalid input. Move digits should be 0-7.')
        else:
            start, end = split_and_convert(inputstr)
            try:
                movetype = self.classify_move(start, end, self.turn, board=kwargs['board'])
            except InvalidMoveError as m:
                raise
            else:
                return start, end, movetype

    def prompt_for_promotion_piece(self, coord, **kwargs):
        piece = kwargs['board'].get_piece(coord)
        upgrade_code = None
        while upgrade_code is not None and upgrade_code not in 'rkbq':
            upgrade_code = kwargs['ui'].get_player_input('Select piece to '
                'promote pawn to (r=Rook, '
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

    def promote_pawns(self, ReplacementPieceClass=Queen, **kwargs):
        for coord in kwargs['board'].get_coords('white', 'pawn'):
            col, row = coord
            if row == 7:
                if self.debug:
                    ReplacementPieceClass = Queen
                else:
                    ReplacementPieceClass = self.prompt_for_promotion_piece(coord)
                # debugmsg(f'{kwargs['board'].get_piece(coord)} at {coord} promoted to {ReplacementPieceClass.name}.')
                self.add(coord, ReplacementPieceClass('white'))
        for coord in kwargs['board'].get_coords('black', 'pawn'):
            col, row = coord
            if row == 0:
                if self.debug:
                    ReplacementPieceClass = Queen
                else:
                    ReplacementPieceClass = self.prompt_for_promotion_piece(coord)
                # debugmsg(f'{kwargs['board'].get_piece(coord)} at {coord} promoted to {ReplacementPieceClass.name}.')
                self.remove(coord)
                self.add(coord, ReplacementPieceClass('black'))

    def valid_move(self, start, end, colour, **kwargs):
        try:
            movetype = self.classify_move(start, end, colour)
        except MoveError as m:
            return False
        else:
            return True

    def classify_move(self, start, end, colour, **kwargs):
        '''
        Checks for the following conditions:
        1. There is a start piece of the player's colour
        2. There is no end piece, or end piece is not of player's colour
        3. The move is a valid castling move
        4. There are no pieces between start and end coord (for Rook, Bishop, Queen)
        5. The move is valid for the selected piece
        6. The move is a valid pawn capture or en passant capture
        
        Returns the type of move, otherwise raises InvalidMoveError
        '''
        def isblocked(start, end):
            piece = kwargs['board'].get_piece(start)
            if piece.name.lower() != 'knight':
                for coord in kwargs['board'].coords_between(start, end):
                    if kwargs['board'].get_piece(coord) is not None:
                        return True
            return False

        def ispawncapture(start, end, colour):
            x, y, dist = vector(start, end)
            own_piece = kwargs['board'].get_piece(start)
            opp_piece = kwargs['board'].get_piece(end)
            if opp_piece is not None \
                    and opp_piece.colour != self.turn \
                    and abs(x) == 1:
                if own_piece.colour == 'white' and y == 1:
                    return True
                elif own_piece.colour == 'black' and y == -1:
                    return True
            return False
        
        def isenpassantcapture(start, end, colour):
            s_col, s_row = start
            e_col, e_row = end
            enpassant_coord = (s_row, e_col)
            own_piece = kwargs['board'].get_piece(start)
            opp_piece = kwargs['board'].get_piece(enpassant_coord)
            # TODO: Use more robust way of checking for 
            # enpassant capture
            if opp_piece is not None \
                    and (self.turn == 'white' and s_row == 4
                        or self.turn == 'black' and s_row == 3) \
                    and opp_piece.colour != self.turn \
                    and opp_piece.moved == 1 \
                    and abs(e_col - s_col) == 1:
                return True
            return False

        def iscastling(start, end, colour):
            start_piece = kwargs['board'].get_piece(start)
            end_piece = kwargs['board'].get_piece(end)
            if not start_piece.name == 'king' or start_piece.moved:
                return False
            x, y, dist = vector(start, end)
            if not (y == 0 and abs(x) == 2):
                return False
            rook_col = 0 if x < 0 else 7
            rook_row = 0 if colour == 'white' else 7
            rook_coord = (rook_col, rook_row)
            rook_piece = kwargs['board'].get_piece(rook_coord)
            if not rook_piece.name == 'rook' or rook_piece.moved:
                return False
            return True

        start_piece = kwargs['board'].get_piece(start)
        end_piece = kwargs['board'].get_piece(end)
        other_colour = 'white' if colour == 'black' else 'black'
        # (1)
        if start_piece is None:
            raise InvalidPieceMovedError(start, end, f'No {self.turn} piece at {start}')
        elif start_piece.colour != colour:
            raise InvalidPieceMovedError(start, end, f'{start_piece} does not belong to player')
        # (2)
        elif end_piece is not None and end_piece.colour == colour:
            raise DestinationIsBlockedError(start, end, f'{end} is occupied by {end_piece}')
        # (3)
        elif iscastling(start, end, colour):
            return 'castling'
        # (4) 
        elif isblocked(start, end):
            raise PathIsBlockedError(start, end, f'Path from {start} to {end} is blocked')
        # (5)
        elif start_piece.isvalid(start, end):
            return 'move'
        # (6)
        elif start_piece.name == 'pawn':
            if ispawncapture(start, end, colour):
                return 'pawncapture'
            elif isenpassantcapture(start, end, colour):
                return 'enpassantcapture'
        raise InvalidMoveError(start, end, f'{start} -> {end}:\nInvalid move for {start_piece}')

    def update(self, start, end, movetype, **kwargs):
        '''Update board information with the player's move.'''
        def ischecked(colour):
            '''
            Return True if <colour> king is checked,
            else return False.
            '''
            for own_king_coord in kwargs['board'].get_coords(colour, 'king'):
                other_colour = 'white' if colour == 'black' else 'black'
                for opp_coord in kwargs['board'].coords(other_colour):
                    try:
                        movetype = self.classify_move(opp_coord,
                                                      own_king_coord,
                                                      other_colour,
                                                      debug = False,
                                                      board=kwargs['board'],
                                                      )
                        # debugmsg(f'{kwargs['board'].get_piece(own_king_coord)} is checked by {kwargs['board'].get_piece(opp_coord)}')
                    except MoveError:
                        return False
            return True

        try:
            movetype = self.classify_move(start, end, self.turn, board=kwargs['board'])
        except MoveError:
            movetype = None
        kwargs['board'].move(start, end, movetype=movetype)
        self.promote_pawns(board=kwargs['board'])
        if ischecked(self.turn):
            kwargs['ui'].set_msg(f'{self.turn} is in check.')

    def next_turn(self):
        '''Hand the turn over to the other player.'''
        if self.turn == 'white':
            self.turn = 'black'
        elif self.turn == 'black':
            self.turn = 'white'

    def winner(self, **kwargs):
        white_king_alive = bool(kwargs['board'].get_coords('white', 'king'))
        black_king_alive = bool(kwargs['board'].get_coords('black', 'king'))
        if white_king_alive and black_king_alive:
            return None
        elif white_king_alive and not black_king_alive:
            return 'white'
        elif not white_king_alive and black_king_alive:
            return 'black'
        else:
            kwargs['ui'].set_msg('Neither king is on the board')



class ChessBoard:
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

    @classmethod
    def coords_between(cls, start, end):
        '''
        Return list of coordinates between start and end coord.
        List does not include start coord but includes end coord.
        Move must be horizontal, vertical, or diagonal only.
        '''
        x, y, dist = vector(start, end)
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

    def add(self, coord, piece):
        '''Add/replace a piece at coord.'''
        if self.position.get(coord, None) is not None:
            del self.position[coord]
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
        
    def as_str(self):
        '''
        Returns the contents of the board
        as a linebreak-delimited string.
        '''
        output = ['   0 1 2 3 4 5 6 7']
        row_ctr = 7
        # Row 7 is at the top, so print in reverse order
        for row in range(7, -1, -1):
            line = f' {row_ctr} '
            row_ctr -= 1
            for col in range(8):
                coord = (col, row)  # tuple
                if coord in self.coords():
                    piece = self.get_piece(coord)
                    line += f'{piece.symbol()}'
                else:
                    piece = None
                    line += ' '
                if col < 7:
                    line += ' '
            output.append(line)
        return output