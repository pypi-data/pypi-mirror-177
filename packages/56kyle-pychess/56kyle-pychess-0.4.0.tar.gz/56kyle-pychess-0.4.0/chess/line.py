import math
from dataclasses import dataclass, replace
from typing import Set, Tuple, Iterable

from chess.direction import Direction
from chess.position import Position


@dataclass(frozen=True)
class Line:
    p1: Position
    p2: Position

    def __post_init__(self):
        self.validate()

    def validate(self):
        self._validate_points_are_different()

    def _validate_points_are_different(self):
        if self.p1 == self.p2:
            raise ValueError(f'p1 and p2 must be different: {self.p1} == {self.p2}')

    @property
    def direction(self) -> 'Direction':
        return Direction(radians=self.p1.theta_to(position=self.p2))

    @property
    def dy(self) -> int:
        return self.p2.rank - self.p1.rank

    @property
    def dx(self) -> int:
        return self.p2.file - self.p1.file

    @property
    def minimum_offset_values(self) -> Tuple[int, int]:
        gcd: int = math.gcd(self.dx, self.dy)
        if gcd == 0:
            return self.dx, self.dy
        return self.dx // gcd, self.dy // gcd

    def __contains__(self, position: Position) -> bool:
        return self.is_colinear(position=position)

    def offset(self, dx: int = 0, dy: int = 0) -> 'Line':
        return replace(self, p1=self.p1.offset(dx=dx, dy=dy), p2=self.p2.offset(dx=dx, dy=dy))

    def iter_positions(self, ) -> Iterable[Position]:
        current_position: Position = self.p1
        while self.is_between_p1_and_p2(position=current_position):
            yield current_position
            current_position: Position = current_position.offset(*self.minimum_offset_values)

    def parallel_to(self, line: 'Line') -> bool:
        return self.direction == line.direction or self.direction == line.direction.opposite

    def is_colinear(self, position: Position) -> bool:
        if self._is_eq_to_p1_or_p2(position=position):
            return True
        return self._is_p1_to_position_parallel_to_p1_to_p2(position=position)

    def _is_eq_to_p1_or_p2(self, position: Position) -> bool:
        return position == self.p1 or position == self.p2

    def _is_p1_to_position_parallel_to_p1_to_p2(self, position: Position) -> bool:
        p1_to_position = Direction(radians=self.p1.theta_to(position=position))
        return p1_to_position == self.direction or p1_to_position == self.direction.opposite

    def is_closer_to_p2_than_p1(self, position: Position) -> bool:
        return self.p1.distance_to(position=position) > self.p2.distance_to(position=position)

    def is_between_p1_and_p2(self, position: Position) -> bool:
        return self._is_between_p1_and_p2_files(position=position) and self._is_between_p1_and_p2_ranks(position=position)

    def _is_between_p1_and_p2_files(self, position: Position) -> bool:
        return min(self.p1.file, self.p2.file) <= position.file <= max(self.p1.file, self.p2.file)

    def _is_between_p1_and_p2_ranks(self, position: Position) -> bool:
        return min(self.p1.rank, self.p2.rank) <= position.rank <= max(self.p1.rank, self.p2.rank)




