class MoveError(Exception):
    def __init__(self, piece, message):
        self.message = message
        self.piece = piece
    
    def __str__(self):
        return f'{self.piece} -> {self.message}'
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
    def __init__(self, **kwargs):
        self.position = {}
        self.debug = kwargs.get('debug',False)

    def coords(self):
        '''Return list of piece coordinates.'''
        return self.position.keys()

    def pieces(self):
        '''Return list of board pieces.'''
        return self.position.values()

    def get_piece(self, coord):
        '''
        Return the piece at coord.
        Returns None if no piece at coord.
        '''
        return self.position.get(coord, None)

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

    def move(self, start, end):
        '''
        Move the piece at start to end.
        Validation should be carried out first
        to ensure the move is valid.
        '''
        piece = self.get_piece(start)
        #print(f'start: {start} end: {end} piece: {piece}')
        self.remove(start)
        self.add(end, piece)

    def save(self):
        '''creates a copy of the board'''
        import copy
        self.copy = copy.copy(self.position)
    
    def undo(self):
        '''Reverts to last saved copy of the board'''
        self.position = self.copy
    
    def get_king(self,colour):
        '''Return the coordinates of King piece'''
        for coord in self.coords():
            piece = self.get_piece(coord)
            if piece.colour == colour and piece.name == 'king':
                return coord
    
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

        self.winner = None
        self.turn = 'white'
        self.other_turn = 'black'
        open('moves.txt', 'w').close()
        
    def display(self):
        '''
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        '''
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order
        if self.debug == True:
            print('== DISPLAY ==')
        for row in range(8, -1, -1):
            
            for col in range(-1, 8):
                coord = (col, row)  # tuple
                if coord in self.coords():
                    piece = self.get_piece(coord)
                    print(f'{piece.symbol()}', end='')
                elif row == 8:
                    if col == -1:
                        print(' ','0 1 2 3 4 5 6 7' ,end='')
                elif col == -1:
                    print(row,end='')   
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
        if self.debug == True:
            print('== PROMPT ==')
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
        
        def is_own_piece(start):
            '''Ensures that there is a start piece of the player's colour selected'''
            start_piece = self.get_piece(start)
            if start_piece is None or start_piece.colour != self.turn:
                return False
            else:
                return True

        while True:
            try:
                inputstr = input(f'{self.turn.title()} player: ')
                if not valid_format(inputstr):
                    print('Invalid input. Please enter your move in the '
                        'following format: __ __, _ represents a digit.')
                elif not valid_num(inputstr):
                    print('Invalid input. Move digits should be 0-7.')
                else:
                    start, end = split_and_convert(inputstr)

                    if is_own_piece(start) and self.valid_move(start, end) and self.move_will_check_own_king(start,end):
                        start_piece = self.get_piece(start)
                        if start_piece.name == 'pawn':
                            start_piece.update_Pawndoublemove(start,end)
                        return start, end
                    else:
                        raise MoveError(self.get_piece(start), 'Invalid move')
            except MoveError:
                print(f'Invalid move for {self.get_piece(start)}')

    def moveclassifier(self, start, end):
        '''
        a method that classfies and returns the move made
        '''
        end_piece = self.get_piece(end)
        if end_piece is not None:
            return 'capture'
        else:
            return 'move'



    def valid_move(self, start, end):
        '''
        Returns True if all conditions are met:
        1. There is no end piece, or end piece is the same colour as start piece
        2. The move is not valid for the selected piece
        
        Returns False otherwise
        '''
        def pawn_isvalid():
            '''
            validation for pawn capture and enpassant
            '''
            x, y, dist = start_piece.vector(start, end)
            iscapture = (x == -1 or x == 1)
            if iscapture and end_piece is None:
                xcord = end[0]
                ycord = start[1]
                sidepiece = self.get_piece((xcord, ycord))
                if sidepiece.name == 'pawn':
                    if not sidepiece.moved:
                        return False
                    
                    else:
                        self.remove((xcord,ycord))
                        return True
                else:
                    return False
            elif not iscapture and end_piece is not None:
                return False
            else:
                return True
        
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if end_piece is not None and end_piece.colour == start_piece.colour:
            return False
        elif not start_piece.isvalid(start, end):
            return False
        elif (start_piece.name == 'queen' or start_piece.name == 'bishop' or start_piece.name == 'rook'):
            if not self.nojump(start,end):
                return False
        elif start_piece.name == 'pawn':
            if not pawn_isvalid():
                return False
        return True

    def move_will_check_own_king(self,start,end):
        '''Returns False if the ally king will be checked after the input move is played'''
        self.save()
        colour = self.get_piece(start).colour
        self.move(start,end)
        validation = not self.is_king_checked(colour)

        self.undo()
        return validation
    
    def coords_moving_between(self,start,end):
        '''Returns a list of positions that the start piece will move accross to reach end'''
        x, y, dist = BasePiece.vector(start, end)
        if x == 0:
            x_dir = 0
        else:
            x_dir = int(x/abs(x))

        if y == 0:
            y_dir = 0
        else:
            y_dir = int(y/abs(y))

        x_pos,y_pos = start
        x_pos += x_dir
        y_pos += y_dir
        output = []

        while (x_pos,y_pos) != end:
            output.append((x_pos,y_pos))
            x_pos += x_dir
            y_pos += y_dir
        
        #print(f'path of {start}: {output}')
        return output


    def nojump(self,start,end):
        '''Returns False if there is a piece between the start and end position'''
        valid = True
        for coords in self.coords_moving_between(start,end):
            if self.get_piece(coords) != None:
                valid = False

        return valid
    
    def promotion(self,end):
        '''When a Pawn has reached the end, it will be replaced with a Queen'''
        piece = self.get_piece(end)
        colour = piece.colour
        if type(piece) == Pawn and (end[1] == 0 or end[1] == 7):
            self.add(end,Queen(colour))

    def get_threat_coords_for(self,input_coords,colour,**kwargs):
        ''' Checks whether the input_coords is threatened by any piece of the input colour
        If return_list=True, Returns a list of input_coords of pieces of input colour which threatens the input_coords'''
        include_king = kwargs.get('include_king',True)
        list_ = []
        for coord in self.coords():
            piece = self.get_piece(coord)
            if piece.colour == colour and (include_king or piece.name != 'king'):
                if self.valid_move(coord, input_coords):
                    #print(f'{item} threatens {input_coords}')
                    list_.append(coord)
        return list_

    def is_king_checked(self,colour,**kwargs):
        '''Checks if the king of the input colour is checked
        If return_checks = True, will also return a list of the positions of pieces checking the king'''

        return_checks = kwargs.get('return_checks',False)

        king_pos = self.get_king(colour)
        checks = self.get_threat_coords_for(king_pos,self.other_colour(colour))
        if return_checks:
            return (checks != []),checks
        else:
            return (checks != [])
    
    def checkmate(self,checks):
        #print(f'checks: {checks}')
        king_pos = self.get_king(self.other_turn)
        checkmate = True
        for check_pos in checks:
            block_positions = self.coords_moving_between(check_pos,king_pos)
            block_positions.append(check_pos)
            for block_pos in block_positions:
                if self.get_threat_coords_for(block_pos,self.other_turn,include_king=False) != []:
                    checkmate = False
        if checkmate:
            king_x,king_y = king_pos
            for x in [(king_x-1),king_x,(king_x+1)]:
                 for y in [(king_y-1),king_y,(king_y+1)]:
                    if x in range(8) and y in range(8):
                        coords = (x,y)
                        if self.valid_move(king_pos,coords):
                            if self.move_will_check_own_king(king_pos,coords):
                                print((king_pos,coords))
                                checkmate = False
                                break
        return checkmate        

    def end(self):
        self.display()
        self.winner = self.turn

    def printmove(self,start,end):
        '''Print the move after its made'''
        a,b = start
        c,d = end
        print(f'{self.get_piece(end)} {a}{b} -> {c}{d}')
        #movelog
        with open('moves.txt','a') as f:
            f.write(f'{self.get_piece(end)} {a}{b} -> {c}{d}\n')

    def update(self, start, end):
        if self.debug == True:
            print('== UPDATE ==')
        '''Update board information with the player's move.'''
        self.remove(end)
        self.move(start, end)
        check,checks = self.is_king_checked(self.other_turn,return_checks = True)
        if check:
            if self.checkmate(checks):
                self.end()
            else:
                print(f'{self.other_turn} is checked')
        self.promotion(end)
        self.printmove(start,end)
        
    def other_colour(self,colour):
        '''Returns the colour that is not the current turn'''
        if colour == 'white':
            return 'black'
        else:
            return 'white'

    def next_turn(self):
        if self.debug == True:
            print('== NEXT TURN ==')
        '''Hand the turn over to the other player.'''
        if self.turn == 'white':
            self.turn = 'black'
        elif self.turn == 'black':
            self.turn = 'white'
        self.other_turn = self.other_colour(self.turn)


class BasePiece:
    name = 'piece'
    moved = False
    def __init__(self, colour):
        if type(colour) != str:
            raise TypeError('colour argument must be str')
        elif colour.lower() not in {'white', 'black'}:
            raise ValueError('colour must be {white, black}')
        else:
            self.colour = colour

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
        return f"King('{self.name}')"

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
        return f"Queen('{self.name}')"

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
        return f"Bishop('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''Bishop can move any number of steps diagonally.'''
        x, y, dist = self.vector(start, end)
        return (abs(x) == abs(y) != 0)


class Knight(BasePiece):
    name = 'knight'
    sym = {'white': '♘', 'black': '♞'}
    def __repr__(self):
        return f"Knight('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''
        Knight moves 2 spaces in any direction, and
        1 space perpendicular to that direction, in an L-shape.
        '''
        x, y, dist = self.vector(start, end)
        return (dist == 3) and (abs(x) != 3 and abs(y) != 3)


class Rook(BasePiece):
    #abc
    name = 'rook'
    sym = {'white': '♖', 'black': '♜'}
    def __repr__(self):
        return f"Rook('{self.name}')"

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
    doublemoveprevturn = False
    def __repr__(self):
        return f"Pawn('{self.name}')"

    def update_Pawndoublemove(self,start,end):
        x, y, dist = self.vector(start, end)
        if abs(y) == 2:
            self.moved = True
        else:
            self.moved = False

    def isvalid(self, start: tuple, end: tuple):
        '''Pawn can only move 1 step forward or 1 step forward and 1 step horizontally when capturing enemy pieces. If pawn moves 2 steps, self.moved is True'''

        x, y, dist = self.vector(start, end)
        if x == -1 or x == 1 or x == 0:
            if self.colour == 'black':
                if start[1] == 6:
                    if y == -2:
                        return (y == -1 or y == -2)
                return (y == -1)
            elif self.colour == 'white':
                if start[1] == 1:
                    if y == 2:
                        return (y == 1 or y == 2)
                return (y == 1)
            else:
                return False
        else:
            return False
    
    def iscapture(self, start: tuple, end: tuple):
        '''
        Return True if pawn captures an enemy piece, else returns False
        '''
        x, y, dist = self.vector(start, end)
        return x == -1 or x == 1
