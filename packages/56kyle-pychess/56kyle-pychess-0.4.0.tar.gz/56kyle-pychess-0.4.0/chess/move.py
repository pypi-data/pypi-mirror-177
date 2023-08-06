

from dataclasses import dataclass, field
from typing import Set, Type, Self

from chess.piece_type import PieceType
from chess.position import Position
from chess.piece import Piece


@dataclass(frozen=True)
class Move:
    piece: Piece
    origin: Position
    destination: Position
    captures: Set[Piece]
    promotion: PieceType | None = None
    additional_moves: Set[Self] = field(default_factory=set)

    def is_promotion(self) -> bool:
        return self.promotion is not None

    def is_capture(self) -> bool:
        return len(self.captures) > 0


