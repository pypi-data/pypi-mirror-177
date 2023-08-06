from abc import ABC
from typing import List

from google.transit import gtfs_realtime_pb2

from marta.api.client import Client
from marta.enums.direction import Direction
from marta.models import (
    LegacyBus,
    RealTimeMapBus,
    GTFSBus,
)


class BusClient(Client, ABC):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def get_buses(self,
                  route: int = None,
                  stop_id: int = None,
                  vehicle_id: int = None,
                  time_point: str = None,
                  direction: Direction = None) -> List[LegacyBus]:
        """
        Query API for bus information

        :param route: route number
        :type route: int, optional
        :param stop_id: Bus stop ID
        :type stop_id: int, optional
        :param vehicle_id: Bus ID
        :type vehicle_id: int, optional
        :param time_point:
        :type time_point: str, optional
        :param direction: Bus direction
        :type direction: Direction, optional
        :return: list of LegacyBus objects
        :rtype: List[LegacyBus]
        """

        if route:
            endpoint = f'/BRDRestService/RestBusRealTimeService/GetBusByRoute/{route}'
        else:
            endpoint = '/BRDRestService/RestBusRealTimeService/GetAllBus'

        # noinspection PyTypeChecker
        buses: List[LegacyBus] = self._legacy_client.get_object(
            url=endpoint,
            model=LegacyBus,
            extract_list=True)

        filtered_buses: List[LegacyBus] = []

        for bus in buses:
            if stop_id and bus.stop_id != stop_id:
                continue
            if vehicle_id and bus.vehicle_id != vehicle_id:
                continue
            if time_point and bus.time_point != time_point:
                continue
            if route and bus.route != route:
                continue
            if direction and bus.direction != direction:
                continue

            filtered_buses.append(bus)

        return filtered_buses

    def get_bus_locations_from_map(self,
                                   vehicle_id: int = None) -> List[RealTimeMapBus]:
        """
        Query API for train information

        :param vehicle_id: Bus ID
        :type vehicle_id: int, optional
        :return: list of RealTimeMapBus objects
        :rtype: List[RealTimeMapBus]
        """
        # noinspection PyTypeChecker
        buses: List[RealTimeMapBus] = self._lab_client.get_object(
            url='/routerapi/routers',
            model=RealTimeMapBus,
            extract_list=True,
        )

        filtered_buses: List[RealTimeMapBus] = []

        for bus in buses:
            if vehicle_id and bus.vehicle_id != vehicle_id:
                continue

            filtered_buses.append(bus)

        return filtered_buses

    def get_bus_locations_from_gtfs(self) -> List[GTFSBus]:
        """
        Query API for bus information

        :return: list of GTFSBus objects
        :rtype: List[GTFSBus]
        """
        feed = gtfs_realtime_pb2.FeedMessage()
        response = self._gtfs_client.get(url='/vehicle/vehiclepositions.pb')
        feed.ParseFromString(response.content)

        return [
            GTFSBus(gtfs_feed_entity=entity) for entity in feed.entity
        ]

    def get_bus_trip_updates_from_gtfs(self):
        """
        Query API for bus information

        :return: list of GTFSBus objects
        :rtype: List[GTFSBus]
        """
        raise NotImplementedError