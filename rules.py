from util import *

KNIGHT_MOVES = (
  (2, 1),
  (2, -1),
  (1, 2),
  (1, -2),
  (-2, 1),
  (-2, -1),
  (-1, 2),
  (-1, -2),
)

KING_MOVES = (
  (0, 1),
  (0, -1),
  (1, 0),
  (-1, 0),
  (1, 1),
  (1, -1),
  (-1, -1),
  (-1, 1)
)

ORTHOGONALS = (
  (1, 0),
  (0, 1),
  (-1, 0),
  (0, -1)
)

DIAGONALS = (
  (1, 1),
  (-1, 1),
  (1, -1),
  (-1, -1)
)

OMNI = ORTHOGONALS + DIAGONALS

def canCapturePieceAt(board, coord, color):
  piece = board.getPieceAt(coord)
  return (piece and piece.getColor() == invertColor(color))

def notBlocked(board, coord, color):
  piece = board.getPieceAt(coord)
  return (not piece) or (piece and piece.getColor() == invertColor(color))

def getPieceMoves(board, coord):
  piece = board.getPieceAt(coord)
  pieceType = piece.getPieceType()
  pieceColor = piece.getColor()
  if pieceType == PAWN:
    return getPawnMoves(board, coord, pieceColor)
  elif pieceType == KNIGHT:
    return getKnightOrKingMoves(board, coord, pieceColor, KNIGHT_MOVES)
  elif pieceType == ROOK:
    return getStraightMoves(board, coord, pieceColor, ORTHOGONALS)
  elif pieceType == BISHOP:
    return getStraightMoves(board, coord, pieceColor, DIAGONALS)
  elif pieceType == QUEEN:
    return getStraightMoves(board, coord, pieceColor, OMNI)
  elif pieceType == KING:
    return getKnightOrKingMoves(board, coord, pieceColor, KING_MOVES)

def getPawnMoves(board, coord, color):
  moves = []
  # What is "forward" depending on color
  forward = ((-1, 0), (1, 0))
  doubleForward = ((-2, 0), (2, 0))
  # 0 for white, 1 for black
  colorIndex = COLORS.index(color)
  # Starting rank based on color
  startingRank = STARTING_RANKS[colorIndex]
  # Coordinates of four main pawn possibilities
  nextSquare = sumCoords(coord, forward[colorIndex])
  skipSquare = sumCoords(coord, doubleForward[colorIndex])
  diagonal1 = sumCoords(nextSquare, (0, -1))
  diagonal2 = sumCoords(nextSquare, (0, 1))
  diagonals = (diagonal1, diagonal2)

  # Check four possibilities: up one, up two, and diagonals
  if not board.getPieceAt(nextSquare):
    moves.append(nextSquare)
  if coord[0] == startingRank and not board.getPieceAt(nextSquare):
    moves.append(skipSquare)
  for d in diagonals:
    if canCapturePieceAt(board, d, color):
      moves.append(d)
  return moves

def getKnightOrKingMoves(board, coord, color, directions):
  moves = []
  for direction in directions:
    potentialSquare = sumCoords(coord, direction)
    if not validCoord(potentialSquare):
      continue
    if notBlocked(board, potentialSquare, color):
      moves.append(potentialSquare)
  return moves

def getStraightMoves(board, coord, color, directions):
  moves = []
  originalCoord = coord
  for direction in directions:
    tempCoord = sumCoords(originalCoord, direction)
    while validCoord(tempCoord):
      if notBlocked(board, tempCoord, color):
        moves.append(tempCoord)
        if canCapturePieceAt(board, tempCoord, color):
          break
      else:
        break
      tempCoord = sumCoords(tempCoord, direction)
  return moves

def allMoves(board, color=None):
  allMoves = []
  pieces = board.getPieces()
  for coord in pieces:
    if color and pieces[coord].getColor() != color:
      continue
    justEndMoves = getPieceMoves(board, coord)
    startEndMoves = [(coord, end) for end in justEndMoves]
    allMoves += startEndMoves
  return allMoves