
from dataclasses import dataclass
from typing import Set

from chess.color import Color
from chess.line import Line
from chess.offset import LINEAR

from chess.piece import Piece
from chess.piece_type import PieceType


class RookType(PieceType):
    name: str = 'Rook'
    letter: str = 'R'
    value: int = 5
    symbol: str = '♜'
    html_decimal: str = '&#9820;'
    html_hex: str = '&#x265C;'

    move_lines: Set[Line] = {offset.as_ray() for offset in LINEAR}
    capture_lines: Set[Line] = {offset.as_ray() for offset in LINEAR}


@dataclass(frozen=True)
class Rook(Piece):
    type: RookType = RookType

@dataclass(frozen=True)
class WhiteRook(Rook):
    color: Color = Color.WHITE

@dataclass(frozen=True)
class BlackRook(Rook):
    color: Color = Color.BLACK

