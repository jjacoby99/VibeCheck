# src/io_models.py
from typing import List
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4

class VibrationPointDTO(BaseModel):
    name: str = ""
    x: float; y: float; z: float
    frequency_h: float = 0.0
    amplitude_h: float = 0.0
    phase_h: float = 0.0
    frequency_v: float = 0.0
    amplitude_v: float = 0.0
    phase_v: float = 0.0

class CuboidDTO(BaseModel):
    length: float = 1.0
    width: float = 1.0
    height: float = 1.0

    @field_validator("length","width","height")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Dimensions must be > 0")
        return v

class SimDTO(BaseModel):
    FPS: int = 30
    total_time: float = 10.0
    time_scale: float = 1.0
    exaggeration: float = 1.0

    @field_validator("FPS", "total_time", "time_scale", "exaggeration")
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("All parameters must be > 0")
        return v

class SessionConfigDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = "Default Config"
    version: int = 1
    blower: CuboidDTO
    sim_props: SimDTO
    measurement_points: List[VibrationPointDTO] = []
