WHITE = 'wh'
BLACK = 'bl'
COLORS = (WHITE, BLACK)

PAWN = 'p'
KNIGHT = 'n'
BISHOP = 'b'
ROOK = 'r'
QUEEN = 'q'
KING = 'k'

BOARD_SIZE = 8

WHITE_PAWN_START_RANK = BOARD_SIZE - 2
BLACK_PAWN_START_RANK = 1
STARTING_RANKS = (WHITE_PAWN_START_RANK, BLACK_PAWN_START_RANK)


STARTING_POS_WHITE = [
  ([6, 0], PAWN),
  ([6, 1], PAWN),
  ([6, 2], PAWN),
  ([6, 3], PAWN),
  ([6, 4], PAWN),
  ([6, 5], PAWN),
  ([6, 6], PAWN),
  ([6, 7], PAWN),
  ([7, 0], ROOK),
  ([7, 1], KNIGHT),
  ([7, 2], BISHOP),
  ([7, 3], QUEEN),
  ([7, 4], KING),
  ([7, 5], BISHOP),
  ([7, 6], KNIGHT),
  ([7, 7], ROOK),
]

STYLIZATIONS = {
  (WHITE, PAWN): "♙",
  (WHITE, ROOK): "♖",
  (WHITE, KNIGHT): "♘",
  (WHITE, BISHOP): "♗",
  (WHITE, QUEEN): "♕",
  (WHITE, KING): "♔",
  (BLACK, PAWN): "♟︎",
  (BLACK, ROOK): "♜",
  (BLACK, KNIGHT): "♞",
  (BLACK, BISHOP): "♝",
  (BLACK, QUEEN): "♛",
  (BLACK, KING): "♚",
}

def coordToAlgebraic(coord):
  letters = 'abcdefgh'
  return letters[coord[1]] + str(8-coord[0])

def codeToName(code):
  if code == WHITE:
    return "white"
  elif code == BLACK:
    return "black"
  elif code == PAWN:
    return "pawn"
  elif code == KNIGHT:
    return "knight"
  elif code == BISHOP:
    return "bishop"
  elif code == ROOK:
    return "rook"
  elif code == QUEEN:
    return "queen"
  elif code == KING:
    return "king"
  else:
    return "???"

def flipCoordAcrossBoard(coord):
  return [BOARD_SIZE-coord[0]-1, coord[1]]

def coordToTuple(l):
  return (l[0], l[1])
  
def sumCoords(c1, c2):
  return (c1[0] + c2[0], c1[1] + c2[1])

def validCoord(coord):
  return coord[0] >= 0 and coord[0] < BOARD_SIZE and coord[1] >= 0 and coord[1] < BOARD_SIZE

def invertColor(color):
  return BLACK if color == WHITE else WHITE

def pprintMoves(moves):
  ret = '| '
  for move in moves:
    ret += f"{coordToAlgebraic(move[0])} to {coordToAlgebraic(move[1])}" + ' | '
  return ret