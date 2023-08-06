
from dataclasses import dataclass

from chess.position import ZERO
from chess.ray import Ray
from chess.segment import Segment


@dataclass(frozen=True)
class Offset:
    dx: int = 0
    dy: int = 0

    def __iter__(self):
        return iter((self.dx, self.dy))

    def __add__(self, other):
        if isinstance(other, Offset):
            return Offset(dx=self.dx + other.dx, dy=self.dy + other.dy)
        else:
            return Offset(dx=self.dx + int(other), dy=self.dy + int(other))

    def __sub__(self, other):
        if isinstance(other, Offset):
            return Offset(dx=self.dx - other.dx, dy=self.dy - other.dy)
        else:
            return Offset(dx=self.dx - int(other), dy=self.dy - int(other))

    def __mul__(self, other):
        if isinstance(other, Offset):
            return Offset(dx=self.dx * other.dx, dy=self.dy * other.dy)
        else:
            return Offset(dx=self.dx * int(other), dy=self.dy * int(other))

    def is_linear(self) -> bool:
        return self.dx == 0 or self.dy == 0

    def is_diagonal(self) -> bool:
        return self.dx != 0 and self.dy != 0

    def as_ray(self) -> 'Ray':
        return Ray(p1=ZERO, p2=ZERO.offset(dx=self.dx, dy=self.dy))

    def as_segment(self) -> 'Segment':
        return Segment(p1=ZERO, p2=ZERO.offset(dx=self.dx, dy=self.dy))


UP = Offset(dx=0, dy=-1)
DOWN = Offset(dx=0, dy=1)
LEFT = Offset(dx=-1, dy=0)
RIGHT = Offset(dx=1, dy=0)

UP_LEFT = UP + LEFT
UP_RIGHT = UP + RIGHT
DOWN_LEFT = DOWN + LEFT
DOWN_RIGHT = DOWN + RIGHT

VERTICAL = {UP, DOWN}
HORIZONTAL = {LEFT, RIGHT}
LINEAR = VERTICAL | HORIZONTAL
DIAGONAL = {UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT}
OMNI = LINEAR | DIAGONAL
