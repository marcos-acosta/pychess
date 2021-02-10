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

DIRECTION_TYPES = [ORTHOGONALS, DIAGONALS]
DIRECTION_PIECES = [[ROOK, QUEEN], [BISHOP, QUEEN]]

def canCapturePieceAt(board, coord, color):
  piece = board.getPieceAt(coord)
  return (piece and piece.getColor() == invertColor(color))

def selfBlocked(board, coord, color):
  piece = board.getPieceAt(coord)
  return piece and piece.getColor() == color

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
    if not selfBlocked(board, potentialSquare, color):
      moves.append(potentialSquare)
  return moves

def getStraightMoves(board, coord, color, directions):
  moves = []
  originalCoord = coord
  for direction in directions:
    tempCoord = sumCoords(originalCoord, direction)
    while validCoord(tempCoord):
      if not selfBlocked(board, tempCoord, color):
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

def getCheckingPieces(board, color=WHITE):
  checkers = []
  oppositeColor = invertColor(color)
  kingCoord = board.getKingCoord(COLORS.index(color))
  forward = [(-1, -1), (-1, 1)] if (color == WHITE) else [(1, -1), (1, 1)]
  # Check for pawn(s)
  for f in forward:
    maybePawn = board.isSpecificPieceAt(sumCoords(kingCoord, f), oppositeColor, PAWN)
    if maybePawn:
      checkers.append(maybePawn)
  # Check for knight(s)
  for knMove in KNIGHT_MOVES:
    maybeKnight = board.isSpecificPieceAt(sumCoords(kingCoord, knMove), oppositeColor, KNIGHT)
    if maybeKnight:
      checkers.append(maybeKnight)
  # Check for king(s)
  for kiMove in KING_MOVES:
    maybeKing = board.isSpecificPieceAt(sumCoords(kingCoord, kiMove), oppositeColor, KING)
    if maybeKing:
      checkers.append(maybeKing)
      break
  # Check for rooks, knights, and queens
  for i, directionType in enumerate(DIRECTION_TYPES):
    dangerPieces = DIRECTION_PIECES[i]
    for direction in directionType:
      tempCoord = sumCoords(kingCoord, direction)
      while validCoord(tempCoord):
        potentialPiece = board.getPieceAt(tempCoord)
        if potentialPiece:
          if potentialPiece.getColor() == oppositeColor and potentialPiece.getPieceType() in dangerPieces:
            checkers.append(potentialPiece)
          break
        tempCoord = sumCoords(tempCoord, direction)
  return checkers
  