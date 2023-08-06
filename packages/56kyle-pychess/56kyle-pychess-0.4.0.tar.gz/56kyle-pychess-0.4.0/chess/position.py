import math
from typing import Protocol
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Position:
    file: int  # 1-indexed
    rank: int  # 1-indexed

    def offset(self, dx: int = 0, dy: int = 0) -> 'Position':
        return replace(self, file=self.file + dx, rank=self.rank + dy)

    def distance_to(self, position: 'Position') -> float:
        return ((self.file - position.file) ** 2 + (self.rank - position.rank) ** 2) ** 0.5

    def theta_to(self, position: 'Position') -> float:
        """Returns the angle in radians between the line from self to position and the x-axis"""
        return math.atan2(position.rank - self.rank, position.file - self.file)

    @classmethod
    def from_fen(cls, fen: str) -> 'Position':
        return cls(file=ord(fen[0]) - 96, rank=int(fen[1]))

    def to_fen(self) -> str:
        return f'{chr(self.file + 96)}{self.rank}'


ZERO = Position(0, 0)

