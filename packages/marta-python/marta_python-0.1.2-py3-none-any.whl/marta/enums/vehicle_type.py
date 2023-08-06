from enum import Enum
from typing import Union

from marta.exceptions import InvalidVehicleTypeError


class VehicleType(Enum):
    BUS = 1
    TRAIN = 2

    @staticmethod
    def from_string(vehicle_type: str) -> Union['VehicleType', None]:
        if not vehicle_type:
            return None

        vehicle_type = vehicle_type.strip().upper()

        if vehicle_type == 'BUS':
            return VehicleType.BUS
        elif vehicle_type == 'TRAIN':
            return VehicleType.TRAIN
        else:
            raise InvalidVehicleTypeError(vehicle_type_provided=vehicle_type)
