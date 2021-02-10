from util import *
from piece import Piece

class Board:
  def __init__(self, pieces=None, kingCoords=[(7,4), (0,4)]):
    if not pieces:
      pieces = self.getInitialPieces()
    self.pieces = pieces
    self.kingCoords = kingCoords

  def copy(self):
    return Board(self.copyPieces(), kingCoords=self.copyKingCoords())

  @staticmethod
  def getInitialPieces():
    pieces = {}
    for coord, pieceType in STARTING_POS_WHITE:
      pieces[coordToTuple(coord)] = Piece(WHITE, pieceType)
      pieces[coordToTuple(flipCoordAcrossBoard(coord))] = Piece(BLACK, pieceType)
    return pieces

  def selfDestruct(self):
    del self.pieces
    del self.kingCoords

  def getPieces(self):
    return self.pieces

  def getKingCoord(self, index):
    return self.kingCoords[index]

  def setKingCoord(self, index, coord):
    self.kingCoords[index] = coord

  def copyKingCoords(self):
    return [self.kingCoords[0], self.kingCoords[1]]

  def squareOccupied(self, coord):
    return coord in self.pieces

  def getPieceAt(self, coord):
    return self.pieces[coord] if (coord in self.pieces) else None

  def deletePieceAt(self, coord):
    del self.pieces[coord]

  def setPieceAt(self, coord, piece):
    self.pieces[coord] = piece

  def isColorPieceAt(self, coord, color):
    if coord in self.pieces:
      piece = self.pieces[coord]
      if piece.getColor() == color:
        return piece
    return False

  def isSpecificPieceAt(self, coord, color, pieceType):
    if coord in self.pieces:
      piece = self.pieces[coord]
      if piece.getColor() == color and piece.getPieceType() == pieceType:
        return piece
    return False

  def movePiece(self, coord1, coord2, inPlace=False):
    if inPlace:
      boardOfInterest = self
    else:
      boardOfInterest = self.copy()
    movePiece = boardOfInterest.getPieceAt(coord1)
    if movePiece.getPieceType() == KING:
      colorIndex = COLORS.index(movePiece.getColor())
      boardOfInterest.setKingCoord(colorIndex, coord2)
    boardOfInterest.deletePieceAt(coord1)
    boardOfInterest.setPieceAt(coord2, movePiece)
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
        