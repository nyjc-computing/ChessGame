class MoveError(Exception):
    pass

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