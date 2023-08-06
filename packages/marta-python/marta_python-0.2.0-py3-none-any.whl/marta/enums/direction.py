from enum import Enum
from typing import Union

from marta.enums.vehicle_type import VehicleType
from marta.exceptions import InvalidDirectionError


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def to_string(self, vehicle_type: VehicleType) -> Union[str, None]:
        if vehicle_type == VehicleType.BUS:
            if self == Direction.NORTH:
                return 'Northbound'
            elif self == Direction.SOUTH:
                return 'Southbound'
            elif self == Direction.EAST:
                return 'Eastbound'
            elif self == Direction.WEST:
                return 'Westbound'
        elif vehicle_type == VehicleType.TRAIN:
            if self == Direction.NORTH:
                return 'N'
            elif self == Direction.SOUTH:
                return 'S'
            elif self == Direction.EAST:
                return 'E'
            elif self == Direction.WEST:
                return 'W'
        else:
            return None

    @staticmethod
    def from_string(direction: str) -> Union['Direction', None]:
        if not direction:
            return None

        direction = direction.strip().upper()

        if direction.startswith('N'):
            return Direction.NORTH
        elif direction.startswith('S'):
            return Direction.SOUTH
        elif direction.startswith('E'):
            return Direction.EAST
        elif direction.startswith('W'):
            return Direction.WEST
        else:
            raise InvalidDirectionError(direction_provided=direction)
