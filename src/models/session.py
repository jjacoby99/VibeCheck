from models.cuboid import Cuboid
from models.point import VibrationPoint
from models.sim import Sim

class SessionModel:
    def __init__(self):
        self.blower: Cuboid | None = None
        self.sim_props: Sim | None = None
        self.measurement_points: list[VibrationPoint] = []