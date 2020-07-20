class MoveError(Exception):

    "MoveError to be raised if the move is an invalid move."

    def __init__(self, message = "Move is invaild."):
        self.message = message


    def __str__(self):
        return f'{self.message}'


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
    def __init__(self):
        self.position = {}

    def coords(self):
        '''Return list of piece coordinates.'''
        return self.position.keys()

    def get_coords(self,name,colour):
        pieces=[]
        for i in self.coords():
            if self.get_piece(i).name==name:
                if self.get_piece(i).colour==colour:
                    pieces.append(i)
        return pieces

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
        self.remove(start)
        self.add(end, piece)
        
        
        '''
        Promote the 'Pawn' piece to a 'Queen' piece when the 'Pawn' piece reaches the opposite end
        '''
        if self.get_piece(end).name == "pawn" and (end[1] == 0 or end[1] == 7):
            self.promote(self.get_piece(end), end)

    def promote(self, piece, end):
        if piece.colour == 'black':
            self.remove(end)
            self.add(end,Queen('black'))
        else:
            self.remove(end)
            self.add(end,Queen('white')) 

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
        
    def display(self):
        '''
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        '''
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order
        
        for row in range(7, -1, -1):
            if row == 7:
                print('a b c d e f g h')
            for col in range(8):
                coord = (col , row)  # tuple
                
                if coord in self.coords():
                    piece = self.get_piece(coord)
                    print(f'{piece.symbol()}', end='')
                #  elif col == 0 and row == 2:
                #     print('2')
                # elif col == 0 and row == 3:
                #     print('3')
                # elif col == 0 and row == 4:
                #     print('4')
                else:
                    piece = None
                    print(' ', end='')

                if col == 7 and row == 7:     # Put line break at the end
                    print(' 8')
                elif col == 7 and row == 6:
                    print(' 7')
                elif col == 7 and row == 5:
                    print(' 6')
                elif col == 7 and row == 4:
                    print(' 5')
                elif col == 7 and row == 3:
                    print(' 4')
                elif col == 7 and row == 2:
                    print(' 3')
                elif col == 7 and row == 1:
                    print(' 2')
                elif col == 7 and row == 0:
                    print(' 1')
                
                
                else:            # Print a space between pieces
                    print(' ', end='')

    def prompt(self):
        '''
        Input format should be two ints,
        followed by a space,
        then another 2 ints
        e.g. 07 27
        '''
        def valid_input(inputstr):
            '''
            Ensure input is 5 characters: 2 numerals,
            followed by a space,
            followed by 2 numerals
            '''
            return len(inputstr) == 5 and inputstr[2] == ' ' \
                and inputstr[0] in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h') \
                and inputstr[3] in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h') \
                and inputstr[1] in ('1', '2', '3', '4', '5', '6', '7', '8') \
                and inputstr[4] in ('1', '2', '3', '4', '5', '6', '7', '8')
        
        def split_and_convert(inputstr):
            '''Convert 5-char inputstr into start and end tuples.'''
            start, end = inputstr.split(' ')
            k = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
            start = (k[start[0]] - 1, int(start[1]) - 1)
            end = (k[end[0]] - 1, int(end[1]) - 1)
            return (start, end)

        while True:
            inputstr = input(f'{self.turn.title()} player: ')
            if not valid_input(inputstr):
                print('Invalid input. Please enter your move in the '
                      'following format: -_ -_, _ represents a digit from 1 to 8, - represents a letter from a-b')
            else:
                start, end = split_and_convert(inputstr)
                if self.valid_move(start, end):
                    print(f'{self.get_piece(start)} to {end}')
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
        if start_piece is None or start_piece.colour != self.turn:
            return False
        elif end_piece is not None and end_piece.colour == self.turn:
            return False
        elif not start_piece.isvalid(start, end):
            return False
        # elif start_piece.name != 'knight':
        #     if check_spaces_btw(start, end):
        #        return False 
        elif self.check(start_piece.colour):
            self.move(start, end)
            if self.check(start_piece.colour):
                self.move(end, start)
                print(f'The {start_piece.colour} king is still in check')
                return False
            self.move(end, start)

        return True

    # def check_spaces_btw(self,start,end):
    #     obstical = False
    #     if start[0] == end[0]: 
    #         #check if piece moves vertically
    #         if start[1]>end[1]:
    #             #moves down
    #             for i in range(end[1]+1,start[1]):
    #                 if self.get_coords((start[0],i)) != None:
    #                     obstical = True
    #         else:
    #             #moves up
    #             for i in range(start[1]+1,end[1]):
    #                 if self.get_coords((start[0],i)) != None:
    #                     obstical = True
    #     elif start[1] == end[1]: 
    #         #check if piece moves horizontally
    #         if start[0]>end[0]:
    #             #moves left
    #             for i in range(end[0]+1,start[0]):
    #                 if self.get_coords((i,start[1])) != None:
    #                     obstical = True
    #         else:
    #             #moves right
    #             for i in range(start[1]+1,end[1]):
    #                 if self.get_coords((i,start[1])) != None:
    #                     obstical = True
    #     else:                  
    #         #at this point the piece is moving
    #         x=start[0]
    #         y=start[1]
    #         if start[0]>end[0]:
    #             #move left
    #             if start[1]>end[1]:
    #                 #move down
    #                 for i in range(start[0],end[0]):
    #                     x-=1
    #                     y-=1
    #                     if self.get_coords((x,y)) != None:
    #                         obstical = True
    #             else:
    #                 #move up
    #                 for i in range(start[0],end[0]):
    #                     x-=1
    #                     y+=1
    #                     if self.get_coords((x,y)) != None:
    #                         obstical = True
    #         else:
    #             #move right
    #             if start[1]>end[1]:
    #                 #move down
    #                 for i in range(start[0],end[0]):
    #                     x+=1
    #                     y-=1
    #                     if self.get_coords((x,y)) != None:
    #                         obstical = True
    #             else:
    #                 #move up
    #                 for i in range(start[0],end[0]):
    #                     x+=1
    #                     y+=1
    #                     if self.get_coords((x,y)) != None:
    #                         obstical = True
    #     return obstical


    def update(self, start, end):
        '''Update board information with the player's move.'''
        self.remove(end)
        self.move(start, end)
        if self.get_coords('king','white')==[]:
            self.winner = 'black'
            return
        if self.get_coords('king','black')==[]:
            self.winner = 'white'
            return
        #this part is for check
        self.check(self.turn)

    def check(self,colour):
        for i in self.coords():
            if colour == 'black':
                if self.get_piece(i).colour == 'black':
                    if self.valid_move(i,self.get_coords('king','white')[0]):
                        print('The white king is in check')
                        return True
            if colour == 'white':
                if self.get_piece(i).colour == 'white':
                    if self.valid_move(i,self.get_coords('king','black')[0]):
                        print('The black king is in check')
                        return True

    def next_turn(self):
        '''Hand the turn over to the other player.'''
        if self.turn == 'white':
            self.turn = 'black'
        elif self.turn == 'black':
            self.turn = 'white'


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
                if start[1] in (0o6,16,26,36,46,56,66,76):
                    return y == -2 or y == -1
                else:
                    return y ==-1

            elif self.colour == 'white':
                if start[1] in (0o1,11,21,31,41,51,61,71): 
                    return (y == 1) or y ==2 
                else:
                    return y ==1
            else:
                return False
        return False
