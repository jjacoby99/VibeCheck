from dataclasses import dataclass, field

@dataclass
class Sim:
    FPS: int = field(default=60)
    exaggeration: float = field(default=1.0)
    time_scale: float = field(default=1.0)
    total_time: float = field(default=10.0)