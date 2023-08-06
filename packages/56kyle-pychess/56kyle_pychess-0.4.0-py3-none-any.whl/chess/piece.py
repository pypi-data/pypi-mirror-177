from dataclasses import dataclass, field, replace, make_dataclass
from typing import Set, Type

from chess.color import Color
from chess.line import Line
from chess.piece_type import PieceType
from chess.position import Position


@dataclass(frozen=True)
class Piece:
    position: Position
    color: Color
    type: PieceType = PieceType
    has_moved: bool = False

    def move(self, position: Position) -> 'Piece':
        return replace(self, position=position, has_moved=True)

    def promote(self, promotion: Type['Piece']) -> 'Piece':
        return replace(self, type=promotion.type)

    def is_ally(self, piece: 'Piece') -> bool:
        return self.color == piece.color

    def is_enemy(self, piece: 'Piece') -> bool:
        return self.color != piece.color

    def get_move_lines(self) -> Set[Line]:
        return self.adjust_lines_to_position(self.type.get_move_lines(
            position=self.position,
            color=self.color,
            has_moved=self.has_moved
        ))

    def get_capture_lines(self) -> Set[Line]:
        return self.adjust_lines_to_position(self.type.get_capture_lines(
            position=self.position,
            color=self.color,
            has_moved=self.has_moved
        ))

    def get_en_passant_lines(self) -> Set[Line]:
        return self.adjust_lines_to_position(self.type.get_en_passant_lines(
            position=self.position,
            color=self.color,
            has_moved=self.has_moved
        ))

    def get_castle_lines(self) -> Set[Line]:
        return self.adjust_lines_to_position(self.type.get_castle_lines(
            position=self.position,
            color=self.color,
            has_moved=self.has_moved
        ))

    def adjust_lines_to_position(self, lines: Set[Line]) -> Set[Line]:
        return {line.offset(dx=self.position.file, dy=self.position.rank) for line in lines}

    def to_fen(self) -> str:
        return f'{self._get_fen_letter()}{self.position.to_fen()}'

    def _get_fen_letter(self) -> str:
        return self.type.letter.lower() if self.color == Color.BLACK else self.type.letter.upper()


