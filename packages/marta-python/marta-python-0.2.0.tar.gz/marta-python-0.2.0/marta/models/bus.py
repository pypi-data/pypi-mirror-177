from datetime import datetime
from typing import Any, List, Optional

from google.transit.gtfs_realtime_pb2 import FeedEntity
from pydantic import Field

from marta.enums.direction import Direction
from marta.models.vehicle import Bus, VehiclePosition


class RealTimeMapBus(Bus):
    vehicle_id_string: str = Field(..., alias='VEHICLE_ID')
    latitude_string: str = Field(..., alias='LATITUDE')
    longitude_string: str = Field(..., alias='LONGITUDE')
    timestamp_history_strings: List[str] = Field(..., alias='TS_HISTORY')

    @property
    def vehicle_id(self) -> int:
        return int(self.vehicle_id_string)

    @property
    def position(self) -> VehiclePosition:
        lat = float(self.latitude_string)
        lon = float(self.longitude_string)
        return VehiclePosition(latitude=lat, longitude=lon)

    @property
    def timestamp_history(self) -> List[datetime]:
        return [datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S%z') for ts in self.timestamp_history_strings]


class LegacyBus(Bus):
    adherence_string: str = Field(..., alias="ADHERENCE")
    block_id_string: str = Field(..., alias="BLOCKID")
    block_abbreviation: str = Field(..., alias="BLOCK_ABBR")
    direction_string: str = Field(..., alias="DIRECTION")
    latitude_string: str = Field(..., alias="LATITUDE")
    longitude_string: str = Field(..., alias="LONGITUDE")
    message_time_string: str = Field(..., alias="MSGTIME")
    route: str = Field(..., alias="ROUTE")
    stop_id_string: str = Field(..., alias="STOPID")
    time_point: str = Field(..., alias="TIMEPOINT")
    trip_id_string: str = Field(..., alias="TRIPID")
    vehicle_id_string: str = Field(..., alias="VEHICLE")

    @property
    def adherence(self) -> int:
        return int(self.adherence_string)

    @property
    def position(self) -> VehiclePosition:
        lat = float(self.latitude_string)
        lon = float(self.longitude_string)
        return VehiclePosition(latitude=lat, longitude=lon)

    @property
    def direction(self) -> Direction:
        return Direction.from_string(direction=self.direction_string)

    @property
    def last_updated(self) -> datetime:
        return datetime.strptime(self.message_time_string, '%m/%d/%Y %I:%M:%S %p')

    @property
    def block_id(self) -> int:
        return int(self.block_id_string)

    @property
    def stop_id(self) -> int:
        return int(self.stop_id_string)

    @property
    def trip_id(self) -> int:
        return int(self.trip_id_string)

    @property
    def vehicle_id(self) -> int:
        return int(self.vehicle_id_string)


class GTFSBus(Bus):
    timestamp: Optional[datetime]
    id: Optional[str]
    label: Optional[str]
    license_plate: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    position: Optional[Any]
    bearing: Optional[float]
    odometer: Optional[float]
    speed: Optional[float]
    trip_id: Optional[str]
    route_id: Optional[str]
    direction_id: Optional[int]
    start_time: Optional[str]
    start_date: Optional[str]
    occupancy_status: Optional[int]
    congestion_level: Optional[int]
    few_seats_available: Optional[int]
    full: Optional[int]
    many_seats_available: Optional[int]
    not_accepting_passengers: Optional[int]
    not_boardable: Optional[int]

    def __init__(self, gtfs_feed_entity: FeedEntity):
        super().__init__()

        self.timestamp = datetime.fromtimestamp(gtfs_feed_entity.vehicle.timestamp)

        # Basic vehicle info
        vehicle_details = gtfs_feed_entity.vehicle.vehicle
        self.id = vehicle_details.id
        self.label = vehicle_details.label
        self.license_plate = vehicle_details.license_plate

        # Position info
        position_details = gtfs_feed_entity.vehicle.position
        self.latitude = position_details.latitude
        self.longitude = position_details.longitude
        self.position = VehiclePosition(latitude=self.latitude, longitude=self.longitude)
        self.bearing = position_details.bearing
        self.odometer = position_details.odometer
        self.speed = position_details.speed

        # Trip info
        trip_details = gtfs_feed_entity.vehicle.trip
        self.trip_id = trip_details.trip_id
        self.route_id = trip_details.route_id
        self.direction_id = trip_details.direction_id
        self.start_time = trip_details.start_time
        self.start_date = trip_details.start_date

        # Occupancy info
        self.occupancy_status = gtfs_feed_entity.vehicle.occupancy_status
        self.occupancy_percentage = gtfs_feed_entity.vehicle.occupancy_percentage
        self.congestion_level = gtfs_feed_entity.vehicle.congestion_level
        self.few_seats_available = gtfs_feed_entity.vehicle.FEW_SEATS_AVAILABLE
        self.full = gtfs_feed_entity.vehicle.FULL
        self.many_seats_available = gtfs_feed_entity.vehicle.MANY_SEATS_AVAILABLE
        self.not_accepting_passengers = gtfs_feed_entity.vehicle.NOT_ACCEPTING_PASSENGERS
        self.not_boardable = gtfs_feed_entity.vehicle.NOT_BOARDABLE
