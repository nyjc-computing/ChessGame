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
    def __init__(self, debug=False):
        self.position = {}
        self.debug = debug

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

    def get_coords(self, **kwargs):
        '''
        Return pieces of specified colour and name
        '''
        coords = []
        
        colour = kwargs.get("colour", False)
        name = kwargs.get("name", False)

        for coord, piece in zip(self.coords(), self.pieces()):
          if colour and name:
            if piece.colour == colour and piece.name == name:
              coords.append(coord)
          elif colour:
            if piece.colour == colour:
              coords.append(coord)
          elif name:
            if piece.name == name:
              coords.append(coord)
          else:
            print("get_coords() requires atleast 1 argument")

        return coords

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
        piece_ = self.get_piece(end)
        piece_.moved = True
        self.log(piece, start, end)
        self.get_piece(end)

    def blocked(self, start, end):
        '''
        Checks coordinates between start and end.
        Returns true if pieces present between else false.
        '''
        x = end[0] - start[0]
        y = end[1] - start[1]
        dir_ = tuple([int(e/abs(e)) if e else 0 for e in (x,y)])
        vector = start

        while True:
          vector = tuple([sum(x) for x in zip(vector, dir_)])
          if vector == end:
            break
          elif self.get_piece(vector):
            return True
        return False

    def check(self, player_colour):
        '''
        Checks possibility of movement between pieces of players to opponent king.
        '''
        opponent_colour = "black" if player_colour == "white" else "white"
        opponent_king_coord = self.get_coords(colour=opponent_colour, name="king")[0]

        for coord in self.get_coords(colour=player_colour):
          if self.valid_move(coord, opponent_king_coord):
            checked = opponent_colour
            print(f"{checked} is checked.")

    def uncheck(self, colour):
        '''
        
        '''
        end = tuple()
 
        while not end:
            for coord, piece in zip(self.coords(), self.pieces()):
                if piece.colour == colour and isinstance(piece, King):
                    end = coord
            for coord, piece in zip(self.coords(), self.pieces()):
                if piece.colour != colour:
                    if self.valid_move(coord, end):
                        return False
            return True
                
    def log(self, piece, start, end):
      '''
      Print move
      Log moves to moves.txt
      '''
      def combine(l):
        return "".join([str(x) for x in l])

      start, end = combine(start), combine(end)
      move = f"{piece} {start} -> {end}"
      print(move)
      with open("moves.txt", "a") as f:
        f.write(move+"\n")


    def promotion(self,coord,colour,new):
        ''' 
        promote a pawn into a rook
        '''
        choices = {'queen':Queen(colour),
                   'knight':Knight(colour),
                   'bishop':Bishop(colour),
                   'rook':Rook(colour)}
        self.remove(coord)
        self.add(coord,choices[new])    

    
    def prompt_for_piece_promotion(self):
        '''
        get input of what the pawn will be promoted to
        '''
        invalid = True
        while invalid:
            print(
                'please choose a piece you want to promote to,the input sould be one of the following:\nqueen knight bishop rook\n')
            
            new = input()
            
            if not new in ['queen','knight','bishop','rook']:
                print('wrong input. the input sould be one          of the following:\n queen knight            bishop rook\n')
            else:
                invalid = False
        return new

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
        open("moves.txt", "w").close()
        
    def display(self):
        '''
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        '''
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order

        if self.debug:
          print("== DISPLAY ==")
        
        for row in range(7, -1, -1):#print the indicating number for column and row
          if row == 7:
            print(" ",end="")
            for num in range(8):
              print(str(num)+" ", end='')
            print('')
            
          for col in range(8):
            if col < 1:
              print(row, end="")
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
        if self.debug:
          print("== PROMPT ==")

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
                if self.valid_move(start, end):
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
        elif start_piece.name != "knight" and self.blocked(start, end):
            return False
        elif not self.uncheck(self.turn):
            return False
        return True

    def update(self, start, end):
        '''
        Update board information with the player's move.
        '''

        if self.debug:
          print("== UPDATE ==")

        start_piece = self.get_piece(start)
        dead = self.get_piece(end)
        self.remove(end)
        self.move(start, end)

        if dead != None:
            if dead.name == "king":
              self.winner = start_piece.colour
              print(f'Game over. {self.winner} player wins!')
            else:
               self.check(self.turn)


        if end[1] == 0 or end[1] == 7:
            if self.get_piece(end).name == 'pawn':
                colour = self.turn
                new = self.prompt_for_piece_promotion()
                self.promotion(end,colour,new)
        
        
    def next_turn(self):
        '''Hand the turn over to the other player.'''
        if self.debug:
          print("== NEXT TURN ==")

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
    moved = False
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
    moved = False
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
    moved = False
    def __repr__(self):
        return f"Bishop('{self.name}')"

    def isvalid(self, start: tuple, end: tuple):
        '''Bishop can move any number of steps diagonally.'''
        x, y, dist = self.vector(start, end)
        return (abs(x) == abs(y) != 0)


class Knight(BasePiece):
    name = 'knight'
    sym = {'white': '♘', 'black': '♞'}
    moved = False
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
    moved = False
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
    moved = False
    def __repr__(self):
        return f"Pawn('{self.name}')"

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
            else:
                return False
        return False
