from dataclasses import dataclass, field
from models.point import Point

@dataclass
class Cuboid:
    length: float = field(default=1.0)
    width: float = field(default=1.0)
    height: float = field(default=1.0)

    @property
    def vertices(self) -> list[Point]:
        return [
            Point(0, 0, 0),
            Point(self.length, 0, 0),
            Point(self.length, self.width, 0),
            Point(0, self.width, 0),
            Point(0, 0, self.height),
            Point(self.length, 0, self.height),
            Point(self.length, self.width, self.height),
            Point(0, self.width, self.height),
        ]