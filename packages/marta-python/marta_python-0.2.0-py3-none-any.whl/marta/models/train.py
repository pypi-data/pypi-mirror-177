from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Any, List, Optional

from pydantic import Field

from marta.enums.direction import Direction
from marta.enums.train_line import TrainLine
from marta.models.vehicle import Train, VehiclePosition


class RealTimeMapTrainPrediction(Train):
    internal_id: str = Field(..., alias="internalId")
    ioc_id: str = Field(..., alias="iocId")
    direction_string: str = Field(..., alias="direction")
    line_string: str = Field(..., alias="line")
    station: str = Field(..., alias="station")
    destination: str = Field(..., alias="destination")
    waiting_seconds: int = Field(..., alias="seconds")
    next_arrival_time_string: str = Field(..., alias="nextArr")

    @property
    def line(self) -> TrainLine:
        return TrainLine.from_string(line_string=self.line_string)

    @property
    def direction(self) -> Direction:
        return Direction.from_string(direction=self.direction_string)

    @property
    def next_arrival(self) -> datetime:
        return datetime.strptime(self.next_arrival_time_string, "%Y-%m-%dT%H:%M:%Sz")

    @property
    def waiting_time(self) -> timedelta:
        return timedelta(seconds=self.waiting_seconds)

    def _match_for_map_train(self, map_train: 'RealTimeMapTrain') -> bool:
        return self.internal_id == map_train.id


class RealTimeMapTrain(Train):
    line_code: str = Field(..., alias='lineCode')
    direction_string: str = Field(..., alias='direction')
    destination: str = Field(..., alias='destination')
    last_ioc_id: str = Field(..., alias='lastIocId')
    last_arrival_track: str = Field(..., alias='lastArrivalTrack')
    last_arrival_location: str = Field(..., alias='lastArrivalLocation')
    last_arrival_time_string: str = Field(..., alias='lastArrivalTime')
    last_track_index: int = Field(..., alias='lastTrackIndex')
    last_position_coordinates: List[float] = Field(..., alias='lastPosition')
    id: str = Field(..., alias='trainId')
    prediction: Optional[RealTimeMapTrainPrediction] = None

    @property
    def line(self) -> TrainLine:
        return TrainLine.from_line_code(train_line_code=self.line_code)

    @property
    def direction(self) -> Direction:
        return Direction.from_string(direction=self.direction_string)

    @property
    def last_arrival_time(self) -> datetime:
        return datetime.strptime(self.last_arrival_time_string, '%Y-%m-%dT%H:%M:%S')

    @property
    def last_position(self) -> VehiclePosition:
        lat = self.last_position_coordinates[0]
        lon = self.last_position_coordinates[1]
        return VehiclePosition(latitude=lat, longitude=lon)


class RealTimeTrain(Train):
    destination: str = Field(..., alias="DESTINATION")
    direction_string: str = Field(..., alias="DIRECTION")
    event_time_string: str = Field(..., alias="EVENT_TIME")
    head_sign: str = Field(..., alias="HEAD_SIGN")
    line_string: str = Field(..., alias="LINE")
    next_arrival_string: str = Field(..., alias="NEXT_ARR")
    station: str = Field(..., alias="STATION")
    id: str = Field(..., alias="TRAIN_ID")
    waiting_seconds_string: str = Field(..., alias="WAITING_SECONDS")
    waiting_time_string: str = Field(..., alias="WAITING_TIME")
    response_timestamp_string: str = Field(..., alias="RESPONSETIMESTAMP")
    longitude_string: str = Field(..., alias="VEHICLELONGITUDE")
    latitude_string: str = Field(..., alias="VEHICLELATITUDE")
    delay: str = Field(..., alias="DELAY")

    @property
    def direction(self) -> Direction:
        return Direction.from_string(self.direction_string)

    @property
    def line(self) -> TrainLine:
        return TrainLine.from_string(line_string=self.line_string)

    @property
    def next_arrival(self) -> datetime:
        return datetime.strptime(self.next_arrival_string, "%Y-%m-%dT%H:%M:%Sz")

    @property
    def waiting_seconds(self) -> int:
        return int(self.waiting_seconds_string)

    @property
    def waiting_time(self) -> timedelta:
        return timedelta(seconds=self.waiting_seconds)

    @property
    def response_timestamp(self) -> datetime:
        return datetime.strptime(self.response_timestamp_string, "%Y-%m-%dT%H:%M:%Sz")

    @property
    def longitude(self) -> float:
        return float(self.longitude_string)

    @property
    def latitude(self) -> float:
        return float(self.latitude_string)
