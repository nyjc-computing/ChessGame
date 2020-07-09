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
        for i in self.position.items():
            piece = i[1]
            if piece.colour == colour and piece.name == 'king':
                return i[0]
    
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
        
        def valid_piece(start):
            start_piece = self.get_piece(start)
            if start_piece is None or start_piece.colour != self.turn:
                return False
            else:
                return True

        while True:
            inputstr = input(f'{self.turn.title()} player: ')
            if not valid_format(inputstr):
                print('Invalid input. Please enter your move in the '
                      'following format: __ __, _ represents a digit.')
            elif not valid_num(inputstr):
                print('Invalid input. Move digits should be 0-7.')
            else:
                start, end = split_and_convert(inputstr)
                # print(f'valid_move: {self.valid_move(start, end)}')
                # print(f'valid_piece: {valid_piece(start)}')
                # print(f'uncheck: {self.uncheck(start, end)}')

                if valid_piece(start) and self.valid_move(start, end) and self.uncheck(start,end):
                    return start, end
                else:
                    print(f'Invalid move for {self.get_piece(start)}.')


    def valid_move(self, start, end):
        '''
        Returns True if all conditions are met:
        1. There is a start piece of the player's colour
        2. There is no end piece, or end piece is not of player's colour
        3. The move is not valid for the selected piece
        
        Returns False otherwise
        '''
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if end_piece is not None and end_piece.colour == start_piece.colour:
            return False
        elif not start_piece.isvalid(start, end):
            return False
        elif (start_piece.name == 'queen' or start_piece.name == 'bishop' or start_piece.name == 'rook'):
            if not self.nojump(start,end):
                return False
        return True

    def uncheck(self,start,end):
        '''Returns True if the king will be checked after the input move is played'''
        self.save()
        colour = self.get_piece(start).colour
        self.move(start,end)
        validation = not self.check(colour)

        self.undo()
        return validation
    
    def path(self,start,end):
        '''Returns a list of positions that the piece will move accorss'''
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

        valid = True
        for pos in self.path(start,end):
            if self.get_piece(pos) != None:
                valid = False

        return valid

    def end(self):
        '''Checks if King piece is eliminated'''
        d = self.pieces()
        counter = 0
        for each in d:
            if each.name == 'king':
                counter += 1
                colour = each.colour
        if counter == 1:
            self.winner = colour
        else:
            pass
    
    def promotion(self,end):
        piece = self.get_piece(end)
        colour = piece.colour
        if type(piece) == Pawn and (end[1] == 0 or end[1] == 7):
            self.add(end,Queen(colour))

    def threaten(self,position,colour,**kwargs):
        ''' Checks whether the input position is threatened by any piece of the input colour
        If return_list=True, Returns a list of positions of pieces of input colour which threatens the input position'''
        return_list = kwargs.get('return_list',False)
        include_king = kwargs.get('include_king',True)
        list_ = []
        for item in self.position.items():
            piece = item[1]
            piece_position = item[0]
            if piece.colour == colour and (include_king or piece.name != 'king'):
                if self.valid_move(piece_position, position):
                    #print(f'{item} threatens {position}')
                    list_.append(piece_position)
        boolean_ = list_ != []
        if return_list:
            return (boolean_,list_)
        else:
            return boolean_

    def check(self,colour,**kwargs):
        '''Checks if the king of the input colour is checked
        If return_checks = True, will also return a list of the positions of pieces checking the king'''
        #print(colour,end=' ')

        return_checks = kwargs.get('return_checks',False)

        king_pos = self.get_king(colour)
        
        if return_checks:
            return self.threaten(king_pos,self.other_colour(colour),return_list=True)
        else:
            return self.threaten(king_pos,self.other_colour(colour))
    
    def checkmate(self):
        check,checks = self.check(self.other_turn,return_checks = True)
        if check:
            #print(f'checks: {checks}')
            king_pos = self.get_king(self.other_turn)
            checkmate = True
            for check_pos in checks:
                block_positions = self.path(check_pos,king_pos)
                block_positions.append(check_pos)
                for block_pos in block_positions:
                    if self.threaten(block_pos,self.other_turn,include_king=False):
                        checkmate = False
            if checkmate:
                king_x,king_y = king_pos
                for x in [(king_x-1),king_x,(king_x+1)]:
                    for y in [(king_y-1),king_y,(king_y+1)]:
                        if x in range(8) and y in range(8):
                            pos = (x,y)
                            if self.valid_move(king_pos,pos):
                                if self.uncheck(king_pos,pos):
                                    print((king_pos,pos))
                                    checkmate = False
                                    break
            
            if checkmate:
                self.display()
                self.winner = self.turn
            else:
                print(f'{self.other_turn} is checked')

    def printmove(self,start,end):
        a,b = start
        c,d = end
        print(f'{self.get_piece(end)} {a}{b} -> {c}{d}')
        pass

    def update(self, start, end):
        if self.debug == True:
            print('== UPDATE ==')
        '''Update board information with the player's move.'''
        self.remove(end)
        self.move(start, end)
        self.end()
        self.checkmate()
        self.promotion(end)
        self.printmove(start,end)
        
    def other_colour(self,colour):
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
    def __repr__(self):
        return f"Pawn('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''Pawn can only move 1 step forward.'''
        x, y, dist = self.vector(start, end)
        if x == 0:
            if self.colour == 'black':
                if start[1] == 6:
                    return (y == -1 or y == -2)
                else:
                    return (y == -1)
            elif self.colour == 'white':
                if start[1] == 1:
                    return (y == 1 or y == 2)
                else:
                    return (y == 1)
            else:
                return False
        return False
