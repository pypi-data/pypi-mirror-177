
from dataclasses import dataclass, replace
from typing import Self, Tuple

from chess.line import Line
from chess.position import Position


@dataclass(frozen=True)
class Rect:
    p1: Position
    p2: Position

    @classmethod
    def from_line(cls, line: Line) -> Self:
        return cls(p1=line.p1, p2=line.p2)

    def __contains__(self, position: Position) -> bool:
        return self._is_within_width(position=position) and self._is_within_height(position=position)

    def _is_within_width(self, position: Position) -> bool:
        return min(self.p1.file, self.p2.file) <= position.file <= max(self.p1.file, self.p2.file)

    def _is_within_height(self, position: Position) -> bool:
        return min(self.p1.rank, self.p2.rank) <= position.rank <= max(self.p1.rank, self.p2.rank)

    @property
    def width(self) -> int:
        return abs(self.p2.file - self.p1.file) + 1

    @property
    def height(self) -> int:
        return abs(self.p2.rank - self.p1.rank) + 1

    def offset(self, dx: int = 0, dy: int = 0) -> Self:
        return replace(self, p1=self.p1.offset(dx=dx, dy=dy), p2=self.p2.offset(dx=dx, dy=dy))








