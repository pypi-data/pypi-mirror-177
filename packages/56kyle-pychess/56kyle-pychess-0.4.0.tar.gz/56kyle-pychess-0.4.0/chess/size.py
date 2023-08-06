
from dataclasses import dataclass, field

from chess.position import Position


@dataclass(frozen=True)
class Size:
    width: int
    height: int

    def __contains__(self, position: Position) -> bool:
        return self._is_within_width(position=position) and self._is_within_height(position=position)

    def _is_within_width(self, position: Position) -> bool:
        return 1 <= position.file <= self.width

    def _is_within_height(self, position: Position) -> bool:
        return 1 <= position.rank <= self.height

