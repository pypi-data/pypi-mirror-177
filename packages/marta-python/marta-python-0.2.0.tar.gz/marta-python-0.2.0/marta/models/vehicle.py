from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from marta.enums.vehicle_type import VehicleType


class Vehicle(BaseModel):
    """Generic Vehicle object that exists to print vehicles as dicts"""

    vehicle_type: Optional[VehicleType] = None

    def __init__(self, vehicle_type: VehicleType, **data: Any):
        super().__init__(**data)
        self.vehicle_type = vehicle_type

    def __str__(self):
        return str(self.__dict__)


class Train(Vehicle):
    def __init__(self, **data: Any):
        super().__init__(vehicle_type=VehicleType.TRAIN, **data)


class Bus(Vehicle):
    def __init__(self, **data: Any):
        super().__init__(vehicle_type=VehicleType.BUS, **data)


class VehiclePosition:
    """Generic VehiclePosition object that exists to print vehicle positions as dicts"""

    def __init__(self, latitude: float, longitude: float, timestamp: datetime = None):
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
