
from dataclasses import dataclass
from typing import Set

from chess.color import Color
from chess.line import Line
from chess.offset import Offset, UP, RIGHT, DOWN, LEFT
from chess.piece import Piece
from chess.piece_type import PieceType


class KnightType(PieceType):
    name: str = 'Knight'
    letter: str = 'N'
    value: int = 3
    symbol: str = '\u2658'
    html_decimal: str = '&#9822;'
    html_hex: str = '&#x2658;'
    offsets: Set[Offset] = {
        UP * 2 + RIGHT,
        UP * 2 + LEFT,
        DOWN * 2 + RIGHT,
        DOWN * 2 + LEFT,
        RIGHT * 2 + UP,
        RIGHT * 2 + DOWN,
        LEFT * 2 + UP,
        LEFT * 2 + DOWN,
    }
    move_lines: Set[Line] = {offset.as_segment() for offset in offsets}
    capture_lines: Set[Line] = {offset.as_segment() for offset in offsets}


@dataclass(frozen=True)
class Knight(Piece):
    type: KnightType = KnightType


@dataclass(frozen=True)
class WhiteKnight(Knight):
    color: Color = Color.WHITE


@dataclass(frozen=True)
class BlackKnight(Knight):
    color: Color = Color.BLACK



