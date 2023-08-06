from dataclasses import dataclass
from typing import Set

from chess.color import Color
from chess.line import Line
from chess.offset import VERTICAL, DIAGONAL

from chess.piece import Piece
from chess.piece_type import PieceType
from chess.position import Position


class PawnType(PieceType):
    name: str = 'Pawn'
    letter: str = 'P'
    value: int = 1
    symbol: str = '\u2659'
    html_decimal: str = '&#9817;'
    html_hex: str = '&#x2659;'

    move_lines: Set[Line] = {offset.as_segment() for offset in VERTICAL}
    first_move_lines: Set[Line] = {(offset * 2).as_segment() for offset in VERTICAL}
    capture_lines: Set[Line] = {offset.as_segment() for offset in DIAGONAL}
    en_passant_lines: Set[Line] = {offset.as_segment() for offset in DIAGONAL}

    @staticmethod
    def filter_lines_to_color(lines: Set[Line], color: Color) -> Set[Line]:
        if color == Color.WHITE:
            return {line for line in lines if line.dy > 0}
        else:
            return {line for line in lines if line.dy < 0}

    @classmethod
    def get_move_lines(cls, position: Position, color: Color, has_moved: bool):
        if has_moved:
            return cls.filter_lines_to_color(cls.move_lines, color)
        else:
            return cls.filter_lines_to_color(cls.move_lines | cls.first_move_lines, color)

    @classmethod
    def get_capture_lines(cls, position: Position, color: Color, has_moved: bool) -> Set[Line]:
        return cls.filter_lines_to_color(cls.capture_lines, color)

    @classmethod
    def get_en_passant_lines(cls, position: Position, color: Color, has_moved: bool) -> Set[Line]:
        return cls.filter_lines_to_color(cls.en_passant_lines, color)


@dataclass(frozen=True)
class Pawn(Piece):
    type: PawnType = PawnType

@dataclass(frozen=True)
class WhitePawn(Pawn):
    color: Color = Color.WHITE

@dataclass(frozen=True)
class BlackPawn(Pawn):
    color: Color = Color.BLACK

