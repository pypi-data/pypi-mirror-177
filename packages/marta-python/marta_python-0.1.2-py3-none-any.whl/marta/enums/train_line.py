from enum import Enum
from typing import Union

from marta.exceptions import InvalidTrainLineError, InvalidTrainLineCodeError


class TrainLine(Enum):
    BLUE = 0
    GREEN = 1
    RED = 2
    GOLD = 3

    def to_string(self) -> Union[str, None]:
        if self == TrainLine.BLUE:
            return 'Blue'
        elif self == TrainLine.GREEN:
            return 'Green'
        elif self == TrainLine.RED:
            return 'Red'
        elif self == TrainLine.GOLD:
            return 'Gold'
        else:
            return None

    @staticmethod
    def from_string(line_string: str) -> Union['TrainLine', None]:
        if not line_string:
            return None

        line_string = line_string.strip().upper()

        if line_string == 'BLUE':
            return TrainLine.BLUE
        elif line_string == 'GREEN':
            return TrainLine.GREEN
        elif line_string == 'RED':
            return TrainLine.RED
        elif line_string == 'GOLD':
            return TrainLine.GOLD
        else:
            raise InvalidTrainLineError(line_provided=line_string)

    def to_line_code(self) -> Union[str, None]:
        if self == TrainLine.BLUE:
            return '1'
        elif self == TrainLine.GREEN:
            return '2'
        elif self == TrainLine.RED:
            return '4'
        elif self == TrainLine.GOLD:
            return '3'
        else:
            return None

    @staticmethod
    def from_line_code(train_line_code: str) -> Union['TrainLine', None]:
        """
        Convert train line code to TrainLine enum

        :param train_line_code: train line code
        :return: TrainLine enum
        """
        if not train_line_code:
            return None

        if train_line_code == '1':
            return TrainLine.BLUE
        elif train_line_code == '2':
            return TrainLine.GREEN
        if train_line_code == '3':
            return TrainLine.GOLD
        elif train_line_code == '4':
            return TrainLine.RED
        else:
            raise InvalidTrainLineCodeError(line_code_provided=train_line_code)
