from models.cuboid import Cuboid
from models.point import VibrationPoint
from models.sim import Sim

class SessionModel:
    def __init__(self):
        self.blower: Cuboid = Cuboid()
        self.sim_props: Sim = Sim()
        self.measurement_points: list[VibrationPoint] = []
        self.run_simulation: bool = False
        self.name = "My Setup"