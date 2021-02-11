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

DIR_PIECES_DICT = {
  ORTHO: [ROOK, QUEEN],
  DIAGO: [BISHOP, QUEEN]
}

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
    return getKnightMoves(board, coord, pieceColor)
  elif pieceType == ROOK:
    return getStraightMoves(board, coord, pieceColor, ORTHOGONALS)
  elif pieceType == BISHOP:
    return getStraightMoves(board, coord, pieceColor, DIAGONALS)
  elif pieceType == QUEEN:
    return getStraightMoves(board, coord, pieceColor, OMNI)
  elif pieceType == KING:
    return getKingMoves(board, coord, pieceColor)

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

  directionPinned = isPinned(board, coord, color)
  forwardPinned = (directionPinned and forward[colorIndex] not in directionPinned)
  # Check four possibilities: up one, up two, and diagonals
  if not board.getPieceAt(nextSquare) and not forwardPinned:
    moves.append((coord, nextSquare))
  if coord[0] == startingRank and not board.getPieceAt(skipSquare) and not forwardPinned:
    moves.append((coord, skipSquare))
  for d in diagonals:
    if canCapturePieceAt(board, d, color) and (not directionPinned or forward[colorIndex] in directionPinned):
      moves.append((coord, d))
  return moves

def getKnightMoves(board, coord, color):
  moves = []
  for direction in KNIGHT_MOVES:
    potentialSquare = sumCoords(coord, direction)
    if not validCoord(potentialSquare):
      continue
    if not selfBlocked(board, potentialSquare, color):
      moves.append((coord, potentialSquare))
  return moves

def getKingMoves(board, coord, color):
  moves = []
  for direction in KING_MOVES:
    potentialSquare = sumCoords(coord, direction)
    if not validCoord(potentialSquare):
      continue
    if not selfBlocked(board, potentialSquare, color) and not wouldMoveCauseCheck(board, (coord, potentialSquare), color):
      moves.append((coord, potentialSquare))
  return moves

def getStraightMoves(board, coord, color, directions):
  moves = []
  originalCoord = coord
  for direction in directions:
    tempCoord = sumCoords(originalCoord, direction)
    while validCoord(tempCoord):
      if not selfBlocked(board, tempCoord, color):
        moves.append((coord, tempCoord))
        if canCapturePieceAt(board, tempCoord, color):
          break
      else:
        break
      tempCoord = sumCoords(tempCoord, direction)
  return moves

def allLegalMoves(board, color=None):
  allMoves = []
  pieces = board.getPieces()
  for coord in pieces:
    if color and pieces[coord].getColor() != color:
      continue
    allMoves += getPieceMoves(board, coord)
  return allMoves

def isPinned(board, coord, color):
  kCoord= board.getKingCoord(COLORS.index(color))
  # Direction from king ==> piece
  relativeKingToPiece = getAlignment(kCoord, coord)
  if not relativePosToKing:
    return None
  dirType, direction = relativeKingToPiece
  tempCoord = sumCoords(coord, direction)
  while validCoord(tempCoord):
    piece = board.getPieceAt(tempCoord)
    if piece:
      if piece.getColor() == invertColor(color) and piece.getPieceType() in DIR_PIECES_DICT[dirType]:
        return (direction, (-direction[0], -direction[1]))
      break
    tempCoord = sumCoords(tempCoord, direction)
  return None

def wouldMoveCauseCheck(board, move, color, getAll=False):
  start, end = move
  testBoard = board.movePiece(start, end, inPlace=False)
  return isInCheck(testBoard, color, getAll=getAll)

def isInCheck(board, color=WHITE, getAll=False):
  checkers = []
  oppositeColor = invertColor(color)
  kingCoord = board.getKingCoord(COLORS.index(color))
  forward = [(-1, -1), (-1, 1)] if (color == WHITE) else [(1, -1), (1, 1)]
  # Check for pawn(s)
  for f in forward:
    maybePawn = board.isSpecificPieceAt(sumCoords(kingCoord, f), oppositeColor, PAWN)
    if maybePawn:
      if getAll:
        checkers.append(maybePawn)
      else:
        return True
  # Check for knight(s)
  for knMove in KNIGHT_MOVES:
    maybeKnight = board.isSpecificPieceAt(sumCoords(kingCoord, knMove), oppositeColor, KNIGHT)
    if maybeKnight:
      if getAll:
        checkers.append(maybeKnight)
      else:
        return True
  # Check for king(s)
  for kiMove in KING_MOVES:
    maybeKing = board.isSpecificPieceAt(sumCoords(kingCoord, kiMove), oppositeColor, KING)
    if maybeKing:
      if getAll:
        checkers.append(maybeKing)
      else:
        return True
  # Check for rooks, knights, and queens
  for i, directionType in enumerate(DIRECTION_TYPES):
    dangerPieces = DIRECTION_PIECES[i]
    for direction in directionType:
      tempCoord = sumCoords(kingCoord, direction)
      while validCoord(tempCoord):
        potentialPiece = board.getPieceAt(tempCoord)
        if potentialPiece:
          if potentialPiece.getColor() == oppositeColor and potentialPiece.getPieceType() in dangerPieces:
            if getAll:
              checkers.append(potentialPiece)
            else:
              return True
          break
        tempCoord = sumCoords(tempCoord, direction)
  if getAll:
    return checkers
  else:
    return False
  