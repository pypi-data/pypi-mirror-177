
from dataclasses import dataclass
from typing import Set

from chess.color import Color
from chess.line import Line
from chess.offset import OMNI

from chess.piece import Piece
from chess.piece_type import PieceType


class QueenType(PieceType):
    name: str = 'Queen'
    letter: str = 'Q'
    value: int = 9
    symbol: str = '♛'
    html_decimal: str = '&#9819;'
    html_hex: str = '&#x265B;'

    move_lines: Set[Line] = {offset.as_ray() for offset in OMNI}
    capture_lines: Set[Line] = {offset.as_ray() for offset in OMNI}


@dataclass(frozen=True)
class Queen(Piece):
    type: QueenType = QueenType

@dataclass(frozen=True)
class WhiteQueen(Queen):
    color: Color = Color.WHITE

@dataclass(frozen=True)
class BlackQueen(Queen):
    color: Color = Color.BLACK

