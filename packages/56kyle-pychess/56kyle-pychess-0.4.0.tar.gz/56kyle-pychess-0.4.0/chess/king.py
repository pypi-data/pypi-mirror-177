
from dataclasses import dataclass
from typing import Set

from chess.color import Color
from chess.line import Line
from chess.offset import HORIZONTAL, OMNI
from chess.piece import Piece
from chess.piece_type import PieceType
from chess.position import Position


class KingType(PieceType):
    name: str = 'King'
    letter: str = 'K'
    value: int = 0
    symbol: str = '♚'
    html_decimal: str = '&#9818;'
    html_hex: str = '&#x265A;'

    move_lines: Set[Line] = {offset.as_segment() for offset in OMNI}
    capture_lines: Set[Line] = move_lines
    castle_lines: Set[Line] = {(offset*2).as_segment() for offset in HORIZONTAL} |\
                              {(offset*3).as_segment() for offset in HORIZONTAL}

    def get_castle_lines(self, position: Position, color: Color, has_moved: bool) -> Set[Line]:
        return set() if has_moved else self.castle_lines


@dataclass(frozen=True)
class King(Piece):
    type: KingType = KingType

@dataclass(frozen=True)
class WhiteKing(King):
    color: Color = Color.WHITE

@dataclass(frozen=True)
class BlackKing(King):
    color: Color = Color.BLACK

