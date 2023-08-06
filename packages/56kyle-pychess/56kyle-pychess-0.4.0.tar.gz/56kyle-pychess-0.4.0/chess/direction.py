import math
from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class Direction:
    """A vector that represents a direction in a 2D plane."""
    radians: float = field(compare=False)

    def __eq__(self, other: 'Direction') -> bool:
        return self._eq_same_theta(other=other)

    def _eq_same_theta(self, other: 'Direction') -> bool:
        return self.theta == other.theta

    def _eq_opposite_theta(self, other: 'Direction') -> bool:
        return self.theta == self.turn_180(theta=other.theta)

    @staticmethod
    def normalize_radians(radians: float) -> float:
        """Adjusts the angle to be between 0 and 2pi"""
        return radians % (2 * math.pi)

    def turn_180(self, theta: float) -> float:
        return self.normalize_radians(radians=theta + math.pi)

    @property
    def theta(self) -> float:
        return self.normalize_radians(self.radians)

    @property
    def opposite(self) -> 'Direction':
        return replace(self, radians=self.turn_180(self.theta))

