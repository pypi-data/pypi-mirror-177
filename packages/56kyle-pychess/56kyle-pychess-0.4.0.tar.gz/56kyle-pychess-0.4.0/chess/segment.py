from dataclasses import dataclass
from typing import Iterable

from chess.line import Line
from chess.position import Position


@dataclass(frozen=True)
class Segment(Line):
    """A Line that extends only between the two points p1 and p2."""

    def __contains__(self, position: Position) -> bool:
        return self.is_colinear(position=position) and self.is_between_p1_and_p2(position=position)

