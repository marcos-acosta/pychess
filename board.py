from util import *
from piece import Piece

class Board:
  def __init__(self, pieces=None, ply=0):
    if not pieces:
      pieces = self.getInitialPieces()
    self.pieces = pieces
    self.ply = ply

  def copy(self):
    return Board(self.copyPieces(), self.ply)

  @staticmethod
  def getInitialPieces():
    pieces = {}
    for coord, pieceType in STARTING_POS_WHITE:
      pieces[coordToTuple(coord)] = Piece(WHITE, pieceType)
      pieces[coordToTuple(flipCoordAcrossBoard(coord))] = Piece(BLACK, pieceType)
    return pieces

  def getPieces(self):
    return self.pieces

  def squareOccupied(self, coord):
    return coord in self.pieces

  def getPieceAt(self, coord):
    return self.pieces[coord] if (coord in self.pieces) else None

  def isColorPieceAt(self, coord, color):
    return (coord in self.pieces and self.pieces[coord].getColor() == color)

  def incrementPly(self):
    self.ply += 1

  def whoseTurn(self):
    return WHITE if self.ply % 2 == 0 else BLACK

  def movePiece(self, coord1, coord2, inPlace=False):
    if inPlace:
      boardOfInterest = self
    else:
      boardOfInterest = self.copy()
    movePiece = boardOfInterest.pieces[coord1]
    del boardOfInterest.pieces[coord1]
    boardOfInterest.pieces[coord2] = movePiece  
    return boardOfInterest

  def copyPieces(self):
    newPieces = {}
    for coord in self.pieces:
      newPieces[coord] = self.pieces[coord].copy()
    return newPieces

  def __repr__(self):
    ret = ''
    for m in range(BOARD_SIZE):
      for n in range(BOARD_SIZE):
        if (m, n) in self.pieces:
          piece = self.pieces[(m, n)]
          ret += STYLIZATIONS[(piece.getColor(), piece.getPieceType())] + ' '
        else:
          ret += '. '
      ret += '\n' if (m < BOARD_SIZE - 1) else ''
    return ret
        