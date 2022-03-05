'''
Chess objects used in the environment.
This script contains definitions for:
1. Move
2. Board
3. Piece - Constructor for building each individual piece
4. Pawn
6. Knight
7. Bishop
8. Rook
9. Queen
10. King
'''

class Move:
    pass

class Board:
    pass

class Piece:
    '''
    Abstract class used to build each Piece Type: Pawn, Knight, Bishop, Rook, Queen, King
    '''
    pass

class Slider(Piece):
    pass

class Leaper(Piece):
    pass

class Pawn(Piece):
    pass

class Knight(Leaper):
    pass

class Bishop(Slider):
    pass

class Rook(Slider):
    pass

class Queen(Slider):
    pass

class King(Slider):
    pass