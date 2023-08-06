from datetime import datetime, time, timedelta
from typing import Any, List, Callable

from pydantic import Field

from marta.enums.direction import Direction
from marta.enums.train_line import TrainLine
from marta.models.vehicle import Train


class Arrivals:
    def __init__(self, arrivals: List['Arrival']):
        self._arrivals = arrivals

    def __iter__(self):
        return iter(self._arrivals)

    def __len__(self):
        return len(self._arrivals)

    def __getitem__(self, item):
        return self._arrivals[item]

    def __repr__(self):
        return self._arrivals.__repr__()

    def __str__(self):
        return self._arrivals.__str__()

    def _filter(self, attribute_name: str, calculation: Callable[[Any], bool]) -> 'Arrivals':
        matching_arrivals = []

        for arrival in self._arrivals:
            if not hasattr(arrival, attribute_name):
                continue

            attribute_value = getattr(arrival, attribute_name)
            if calculation(attribute_value):
                matching_arrivals.append(arrival)

        return Arrivals(arrivals=matching_arrivals)

    def on_line(self, line: TrainLine) -> 'Arrivals':
        return self._filter(attribute_name='line', calculation=lambda _line: _line == line)

    def going_to(self, destination: str) -> 'Arrivals':
        return self._filter(attribute_name='destination', calculation=lambda _destination: _destination == destination)

    def arriving_at(self, station: str) -> 'Arrivals':
        return self._filter(attribute_name='station', calculation=lambda _station: _station == station)

    def heading(self, direction: Direction) -> 'Arrivals':
        return self._filter(attribute_name='direction', calculation=lambda _direction: _direction == direction)

    def with_wait_less_than(self, wait: timedelta) -> 'Arrivals':
        return self._filter(attribute_name='wait', calculation=lambda _wait: _wait < wait)

    def with_wait_greater_than(self, wait: timedelta) -> 'Arrivals':
        return self._filter(attribute_name='wait', calculation=lambda _wait: _wait > wait)

    def arriving_now(self) -> 'Arrivals':
        return self._filter(attribute_name='arriving', calculation=lambda _arriving: _arriving is True)

    def arrived(self) -> 'Arrivals':
        return self._filter(attribute_name='arrived', calculation=lambda _arrived: _arrived is True)


class Arrival(Train):
    """
    Represents an arriving train at a given station.
    """
    destination: str = Field(..., alias='DESTINATION')
    direction_string: str = Field(..., alias='DIRECTION')
    event_time_string: str = Field(..., alias='EVENT_TIME')
    line_string: str = Field(..., alias='LINE')
    next_arrival_string: str = Field(..., alias='NEXT_ARR')
    station: str = Field(..., alias='STATION')
    id: str = Field(..., alias='TRAIN_ID')
    waiting_seconds_string: str = Field(..., alias='WAITING_SECONDS')
    waiting_time_string: str = Field(..., alias='WAITING_TIME')

    def __init__(self, **data: Any):
        super().__init__(**data)

    @property
    def direction(self) -> Direction:
        return Direction.from_string(direction=self.direction_string)

    @property
    def line(self) -> TrainLine:
        return TrainLine.from_string(line_string=self.line_string)

    @property
    def last_updated(self) -> datetime:
        return datetime.strptime(self.event_time_string, '%m/%d/%Y %I:%M:%S %p')

    @property
    def next_arrival(self) -> time:
        return datetime.strptime(self.next_arrival_string, '%I:%M:%S %p').time()

    @property
    def waiting_seconds(self) -> int:
        return int(self.waiting_seconds_string)

    @property
    def waiting_time(self) -> timedelta:
        if self.waiting_seconds_string.strip().lower() in ['arriving', 'arrived']:
            return timedelta(seconds=0)
        return timedelta(seconds=self.waiting_seconds)

    @property
    def arriving(self) -> bool:
        return self.waiting_time_string.strip().lower() == 'arriving'

    @property
    def arrived(self) -> bool:
        return self.waiting_time_string.strip().lower() == 'arrived'
