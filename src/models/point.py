from dataclasses import dataclass, field

@dataclass
class Point:
    x: float = field(default=0.0)
    y: float = field(default=0.0)
    z: float = field(default=0.0)

    name: str = field(default="")
    
@dataclass
class VibrationPoint(Point):
    frequency_h: float = field(default=0.0) # hz
    amplitude_h: float = field(default=0.0) # m
    phase_h: float = field(default=0.0) # radians

    frequency_v: float = field(default=0.0) # hz
    amplitude_v: float = field(default=0.0) # m
    phase_v: float = field(default=0.0) # radians
