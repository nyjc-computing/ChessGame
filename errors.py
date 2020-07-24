class MoveError(Exception):
    def __init__(self, start, end, msg):
        self.start = start
        self.end = end
        self.msg = msg

        super().__init__(f'{start} -> {end}: {self.msg}')

class InvalidPieceMovedError(MoveError):
    pass

class DestinationIsBlockedError(MoveError):
    pass

class PathIsBlockedError(MoveError):
    pass

class InvalidMoveError(MoveError):
    pass

class InvalidPawnCaptureError(InvalidMoveError):
    pass

class InvalidCastlingError(InvalidMoveError):
    pass