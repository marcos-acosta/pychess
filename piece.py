from util import *

class Piece:
  def __init__(self, color=WHITE, pieceType=PAWN):
    self.color = color
    self.pieceType = pieceType

  def copy(self):
    return Piece(self.color, self.pieceType)

  def __repr__(self):
    return f"{codeToName(self.color)} {codeToName(self.pieceType)}"

  def getColor(self):
    return self.color

  def getPieceType(self):
    return self.pieceType