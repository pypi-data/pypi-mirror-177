

from dataclasses import dataclass

from chess.line import Line
from chess.position import Position


@dataclass(frozen=True)
class Ray(Line):
    """A Line that extends only in the direction of the vector from p1 to p2."""

    def __contains__(self, position: Position) -> bool:
        return self.is_colinear(position=position) and self.is_on_or_beyond_ray(position=position)

    def is_on_or_beyond_ray(self, position: Position) -> bool:
        return self.is_between_p1_and_p2(position=position) or self.is_closer_to_p2_than_p1(position=position)


