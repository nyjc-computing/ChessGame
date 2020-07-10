import copy

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
        if 'debug' in kwargs.keys():
            if kwargs['debug'] == True:
                self.debug = True
            else:
                self.debug = False
        else:
            self.debug = False  
        

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
        piece.moved = True
        self.remove(start)
        self.add(end, piece)

    def start(self):
        '''Set up the pieces and start the game. Create CSV file movelog_file.'''
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
        self.winner = None

        f = open('movelog_file', 'w')
        f.close()

        
    def display(self):
        '''
        Displays the contents of the board.
        Each piece is represented by a coloured symbol.
        '''
        # helper function to generate symbols for piece
        # Row 7 is at the top, so print in reverse order
        # Row 8 is for column labels, Column -1 is for Row labels
        for row in range(8, -1, -1):
            for col in range(-1, 8):
                coord = (col, row)  # tuple
                if coord in self.coords():
                    piece = self.get_piece(coord)
                    print(f'{piece.symbol()}', end='')
                elif row == 8:
                  if col == -1:
                    print(' ', end='')
                  else:
                    print(f'{col}', end='')
                elif col == -1:
                  print(f'{row}', end='')
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
                and inputstr[0:1].isdigit() \
                and inputstr[3:4].isdigit()
        
        def valid_num(inputstr):
            '''Ensure all inputted numerals are 0-7.'''
            for char in (inputstr[0:1] + inputstr[3:4]):
                if char not in '01234567':
                    return False
            return True
        
        def split_and_convert(inputstr):
            '''Convert 5-char inputstr into start and end tuples.'''
            start, end = inputstr.split(' ')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))
            return (start, end)

        def printmove(start, end):
            '''Print the player\'s move'''
            if self.castling(start, end):
                return f'{self.turn} castling.'
            else:
                a,b = start
                c,d = end
                movedpiece = str(self.get_piece(start))
                return f'{movedpiece} {a}{b} -> {c}{d}'
            
        def movelog(start, end):
            '''
            Save all moves made into the CSV file movelog_file
            '''
            with open('movelog_file', 'a') as f:
                f.write(f'\n{printmove(start, end)}')

        while True:
            inputstr = input(f'{self.turn.title()} player: ')
            if not valid_format(inputstr):
                print('Invalid input. Please enter your move in the '
                      'following format: __ __, _ represents a digit.')
            elif not valid_num(inputstr):
                print('Invalid input. Move digits should be 0-7.')
            else:
                start, end = split_and_convert(inputstr)
                if self.temp_check(self.turn, start, end):
                    print(f"Invalid move, {self.turn} King is in check")
                elif self.valid_move(start, end):
                    print(printmove(start, end))
                    self.previousmove = (start, end)
                    print(self.moveclassifier(start,end))
                    return start, end
                else:
                    print(f'Invalid move for {self.get_piece(start)}.')

    def valid_move(self, start, end):
        '''

        Returns True if all conditions are met:
        1. There is a start piece of the player's colour
        2. There is no end piece, or end piece is not of player's colour
        3. The move is not invalid for the selected piece
        4. There is no moving over other pieces
        Returns False otherwise
        5. Special moves
        '''
        def pawn_isvalid():
          """
          Extra validation for pawn capturing and en passant moves
          Returns True if move is valid, else returns False
          """
          is_capture = start_piece.is_capture(start, end)
          if is_capture and end_piece is None:
            xcord = end[0]
            ycord = start[1]
            sidepiece = self.get_piece((xcord, ycord))
            if sidepiece.name == 'pawn':
              if not sidepiece.doublemoveprevturn:
                return False
              elif (xcord, ycord) == self.previousmove[1]:
                self.move((xcord, ycord), end)
                return True
              else:
                return False
            else:
              return False
          elif not is_capture and end_piece is not None:
            return False
          else:
            return True

        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if self.castling(start, end):
            print('valid move')
            return True
        elif start_piece is None or start_piece.colour != self.turn:
            return False
        elif end_piece is not None and end_piece.colour == self.turn:
            return False
        elif not start_piece.isvalid(start, end):
            return False

        elif start_piece.name == 'pawn':
          if not pawn_isvalid():
            return False
        elif not self.nojumpcheck(start, end):

            return False
        return True
        
    def nojumpcheck(self, start, end):
        '''
        self.nojumpcheck(start, end)
        
        check if the piece moved will move over another piece
        return boolean:
        False if jumping over happens
        else True
        yuheng
        '''
        x = end[0]- start[0]
        y = end[1]- start[1]
        position_checking = start
        nojump = True
        if abs(x) == 1 or abs(y) == 1:
            nojump = True
        elif x == 0:
            # moving vertically
            for i in range(0, abs(y)-1):
                position_checking = list(position_checking)
                position_checking[1] += y/abs(y)
                position_checking = tuple(position_checking)
                if self.get_piece(position_checking) != None:
                    nojump = False
        elif y == 0:
            # moving horizontally
            for i in range(0, abs(x)-1):
                position_checking = list(position_checking)
                position_checking[0] += x/abs(x)
                position_checking = tuple(position_checking)
                if self.get_piece(position_checking) != None:
                    nojump = False
        else:
            # moving diagonally
            for i in range(0, abs(x)-1):
                position_checking = list(position_checking)
                position_checking[0] += x/abs(x)
                position_checking[1] += y/abs(y)
                position_checking = tuple(position_checking)
                if self.get_piece(position_checking) != None:
                    nojump = False
        return nojump

    def castling(self, start, end):
        '''
        special move: castling
        1. The king and the chosen rook are on the player's first rank.
        2. Neither the king nor the chosen rook has previously moved.
        3. There are no pieces between the king and the chosen rook.
        4. The king is not currently in check.
        5. The king does not pass through a square that is attacked by an enemy piece.
        returns boolean:
        if castling move is valid return True
        else return False
        yuheng
        '''
        start_piece = self.get_piece(start)
        end_piece = self.get_piece(end)
        if start_piece == None or end_piece == None:
            return False
        elif start_piece.colour != end_piece.colour:
            return False
        elif start_piece.moved or end_piece.moved:
            return False
        elif not ((start_piece.name == 'king' and end_piece.name == 'rook') or (start_piece.name == 'rook' and end_piece.name == 'king')):
            return False
        elif not self.nojumpcheck(start, end):
            return False
        else:
            if start_piece.name == 'king':
                king_pos = start
                rook_pos = end
            else:
                king_pos = end
                rook_pos = start
            if self.check(self.turn) == True:
                return False
            else:
                x = rook_pos[0] - king_pos[0]
                position_checking = king_pos
                for i in range(0, 2):
                    position_checking = list(position_checking)
                    position_checking[0] += x/abs(x)
                    print(type(position_checking[0]))
                    position_checking = tuple(position_checking)
                    self.add(position_checking, King(self.turn))
                    if self.check(self.turn) == True:
                        self.remove(position_checking)
                        return False
                    self.remove(position_checking)
                return True

    def castlingmove(self, start, end):
        start_piece = self.get_piece(start)
        if start_piece.name == 'king':
            king_pos = start
            rook_pos = end
        else:
            king_pos = end
            rook_pos = start
        x = rook_pos[0] - king_pos[0]
        king_pos_end = list(king_pos)
        king_pos_end[0] += 2*(x/abs(x))
        king_pos_end = tuple(king_pos_end)
        self.move(king_pos, king_pos_end)
        rook_pos_end = list(rook_pos)
        rook_pos_end[0] = king_pos_end[0] - x/abs(x)
        rook_pos_end = tuple(rook_pos_end)
        self.move(rook_pos, rook_pos_end)

    def winnercheck(self):
        '''check for winner'''
        no_of_kings = 0
        for pieces in list(self.pieces()):
            if pieces.name == 'king':
              no_of_kings += 1
        if no_of_kings != 2:
            self.winner = self.turn
    
    def promotioncheck(self):
        '''check for pawn promotion'''
        for coord , piece in self.position.items():
            if piece.name == "pawn" and (coord[1] == 0 or coord[1] == 7):
                self.position[coord] = Queen(piece.colour)

    def separate_pieces(self):
        """
        Separates the coords list into white and black pieces.
        and identify the king

        result is a tuple, with four element,
        list of white pieces and coordinates, list of black pieces and coordinate, white king coord, black king coords
        """
        pieces_coords_list = list(self.coords())
        white_pieces_list = []
        black_pieces_list = []
        white_king_coord = None
        black_king_coord = None
        for coord in pieces_coords_list:
            piece = self.get_piece(coord)
            if piece.colour == 'white':
                if type(piece) == King:
                    white_king_coord = coord
                white_pieces_list.append((piece, coord))
            else:
                if type(piece) == King:
                    black_king_coord = coord
                black_pieces_list.append((piece, coord))

        return (white_pieces_list, black_pieces_list, white_king_coord, black_king_coord)

    def find_attacking_pieces(self, colour):
        """
        Find the pieces attacking the king of the colour given
        """
        if self.debug:
            print("Finding attacking pieces")
        if colour == 'white':
            _ , opponent_pieces_list, own_king_coord, _ = self.separate_pieces()
        else:
            opponent_pieces_list, _ , _ ,  own_king_coord = self.separate_pieces()

        intial_turn = self.turn
        self.turn = 'white' if colour == 'black' else 'black'

        self.attacking_pieces = []
        for (piece, start_coord) in opponent_pieces_list:
            if self.valid_move(start_coord, own_king_coord):
                self.attacking_pieces.append((piece, start_coord))

        self.turn = intial_turn
        

    def check(self, colour):
        """
        self.check(colour)

        the colour argument tells which king to check if it is checked. Assuming that it is a validated move (except if the move would result in check)
        return boolean
        """
        # get all the pieces
        if self.debug:
            print(f"Now checking if the {colour} king is being checked")

        self.find_attacking_pieces(colour)
        if self.debug:
            print("Attacking pieces:", self.attacking_pieces)
        if len(self.attacking_pieces) == 0:
            return False
        return True
    
    def temp_check(self, colour, start, end):
        """
        Create a tempBoard and check if the new move would result in a check.
        """
        if self.debug:
            print("\n\nCreating tempBoard, checking if it will result in check")
        tempBoard = Board(debug = self.debug)
        tempBoard.start()
        tempBoard.position = copy.deepcopy(self.position)
        if tempBoard.valid_move(start,end):
            tempBoard.update(start,end)
        if self.debug:
            print(f"\nprint updated tempBoard display: \n")
            tempBoard.display()
        if tempBoard.check(colour):
            return True
        return False


    def checkmate(self, colour):
        """
        self.checkmate(colour)

        Check if the colour is in checkmate 

        Steps:
        1. if there are two attacking pieces, King must move away,

        2. if only one attacking piece, see if king can move away or
        see if any other pieces are able to block/eat it

        3. see if it will now result in check, if it does not, it will not checkmate

        if king is only piece, 
        """
        if self.debug:
            print("\nChecking for checkmate")
        if colour == 'white':
            own_pieces_list , _, own_king_coord, _ = self.separate_pieces()
        else:
            _, own_pieces_list, _ , own_king_coord = self.separate_pieces()

        # Generating possible king moves
        temp_king_move = set()
        temp_king_move.add((own_king_coord[0] - 1, own_king_coord[1] - 1))
        temp_king_move.add((own_king_coord[0] - 1, own_king_coord[1]))
        temp_king_move.add((own_king_coord[0] - 1, own_king_coord[1] + 1))
        temp_king_move.add((own_king_coord[0], own_king_coord[1] - 1))
        temp_king_move.add((own_king_coord[0], own_king_coord[1] + 1))
        temp_king_move.add((own_king_coord[0] + 1, own_king_coord[1] - 1))
        temp_king_move.add((own_king_coord[0] + 1, own_king_coord[1]))
        temp_king_move.add((own_king_coord[0] + 1, own_king_coord[1] + 1))
        

        # make sure that the end position is in board
        possible_king_move = set()
        for coord in temp_king_move:
            x, y = coord
            if ((0 <= x <= 7) and (0 <= y <= 7)):
                possible_king_move.add(coord)
        if self.debug:
            print("Possible king move set:", possible_king_move)

        # See if king can move or capture
        if self.debug:
            print("\nChecking for possible move")
        for end_coord in possible_king_move:
            if self.debug:
                print(f"checking for move {own_king_coord} -> {end_coord}", end_coord)
            if self.valid_move(own_king_coord, end_coord) and not self.temp_check(colour, own_king_coord, end_coord):
                if self.debug:
                    print(f"VALID MOVE FOUND: {own_king_coord} -> {end_coord}")
                return False
        
        # if king is the only piece left, if king cannot move, checkmate
        # If attacking pieces is more than 2, and king cannot move away, checkmate
        if len(self.attacking_pieces) >= 2 or len(own_pieces_list) == 1:
            return True

        # For only one piece attacking.
        # Check if it can be eaten.
        for _, coord in own_pieces_list:
            if self.valid_move(coord, self.attacking_pieces[0][1]) and not self.check(colour):
                return False

        # Get all attacking piece valid_move square
        valid_move_set = set()
        attacking_piece = self.attacking_pieces[0][0]
        attacking_piece_coord = self.attacking_pieces[0][1]
        for coord in [(i,j) for i in range(8) for j in range(8)]:
            if attacking_piece.isvalid(attacking_piece_coord, coord):
                valid_move_set.add(coord)

        # See if any piece can block it.
        print('\nSee if any move can block it')
        for piece, coord in own_pieces_list:
            for move in valid_move_set:
                if self.valid_move(coord, move) and not self.temp_check(colour, coord, move):
                    if self.debug:
                        print(f"VALID MOVE FOUND: {coord} -> {move}")
                    return False
        return True

    def moveclassifier(self, start, end):
        """
        a method that classifies and returns the type of move being made.
        """
        end_piece = self.get_piece(end)
        if self.castling(start, end):
            return 'castling'
        elif end_piece is not None:
            return 'capture'
        else:
            return 'move'

    def update(self, start, end):
        '''Update board information with the player's move.'''
        if self.castling(start, end):
            self.castlingmove(start, end)
        else:
            self.remove(end)
            self.move(start, end)
        self.winnercheck()
        self.promotioncheck()

    def next_turn(self):
        '''Hand the turn over to the other player.'''
        if self.winner is None:
            if self.turn == 'white':
                self.turn = 'black'
            elif self.turn == 'black':
                self.turn = 'white'
        print(f'\nChecking before prompting the {self.turn} player')
        self.find_attacking_pieces(self.turn)
        if self.checkmate(self.turn):
            self.winner = 'white' if self.turn == 'black' else 'black'
        elif self.check(self.turn):
                print(f"{self.turn} King is in check")


class BasePiece:
    name = 'piece'
    def __init__(self, colour, moved = False):
        if type(colour) != str:
            raise TypeError('colour argument must be str')
        elif colour.lower() not in {'white', 'black'}:
            raise ValueError('colour must be {white, black}')
        else:
            self.colour = colour
            self.moved = moved

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
    doublemoveprevturn = False
    def __repr__(self):
        return f"Pawn('{self.name}')"
    

    def isvalid(self, start: tuple, end: tuple):
        '''
        Pawn can only move 1 step forward into empty space, or 1 step horizontally and 1 step forward while capturing.
        Attribute self.doublemoveprevturn is True when the Pawn moves 2 spaces. Else self.doublemoveprevturn is False

        Ryan - PawnCapture enpassant
        '''
        x, y, dist = self.vector(start, end)
        if x == -1 or x == 1 or x == 0:
          if self.colour == 'black':
            self.doublemoveprevturn = False
            if start[1] ==  6:
              if y == -2:
                self.doublemoveprevturn = True
              return (y == -1 or y == -2)
            return (y == -1)
          elif self.colour == 'white':
            self.doublemoveprevturn = False
            if start[1] ==  1:
                if y == 2:
                  self.doublemoveprevturn = True
                return (y == 1 or y == 2)
            return (y == 1)
          else:
            return False
        else:
            return False
    def is_capture(self, start: tuple, end: tuple):
      """
      Returns True if pawn makes a horizontal move in any direction (a capturing move). Else returns False
      """
      x, y, dist = self.vector(start, end)
      if x == -1 or x == 1:
        return True
      else:
        return False



class MoveError(Exception):
  """
  Raised when an invalid move is made.
  """
pass