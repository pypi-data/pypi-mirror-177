from typing import Set

from chess.color import Color
from chess.line import Line
from chess.position import Position


class PieceType:
    name: str
    letter: str
    value: int
    symbol: str
    html_decimal: str
    html_hex: str

    move_lines: Set[Line] = set()
    capture_lines: Set[Line] = set()
    en_passant_lines: Set[Line] = set()
    castle_lines: Set[Line] = set()

    def to_fen(self) -> str:
        return self.letter

    @classmethod
    def get_move_lines(cls, position: Position, color: Color, has_moved: bool) -> Set[Line]:
        return cls.move_lines

    @classmethod
    def get_capture_lines(cls, position: Position, color: Color, has_moved: bool) -> Set[Line]:
        return cls.capture_lines

    @classmethod
    def get_en_passant_lines(cls, position: Position, color: Color, has_moved: bool) -> Set[Line]:
        return cls.en_passant_lines

    @classmethod
    def get_castle_lines(cls, position: Position, color: Color, has_moved: bool) -> Set[Line]:
        return cls.castle_lines


