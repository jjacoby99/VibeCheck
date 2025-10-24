from models.io_models import SessionConfigDTO, CuboidDTO, SimDTO, VibrationPointDTO
from models.session import SessionModel
from models.cuboid import Cuboid
from models.sim import Sim
from models.point import VibrationPoint

def domain_to_dto(session: SessionModel) -> SessionConfigDTO:
    return SessionConfigDTO(
        name=getattr(session, "name", "Untitled"),
        blower=CuboidDTO(**vars(session.blower)),
        sim_props=SimDTO(**vars(session.sim_props)),
        measurement_points=[VibrationPointDTO(**vars(p)) for p in session.measurement_points],
    )

def dto_to_domain(dto: SessionConfigDTO) -> SessionModel:
    s = SessionModel()
    s.blower = Cuboid(**dto.blower.model_dump())
    s.sim_props = Sim(**dto.sim_props.model_dump())
    s.measurement_points = [VibrationPoint(**mp.model_dump()) for mp in dto.measurement_points]
    setattr(s, "name", dto.name)
    setattr(s, "id", dto.id)  # handy for updates
    return s
