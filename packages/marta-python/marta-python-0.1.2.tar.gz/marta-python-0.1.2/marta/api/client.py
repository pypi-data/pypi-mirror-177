from typing import List

import objectrest
from google.transit import gtfs_realtime_pb2

from marta.enums.direction import Direction
from marta.enums.train_line import TrainLine
from marta.models import (
    LegacyBus,
    LegacyTrain,
    RealTimeTrain,
    RealTimeMapTrain,
    RealTimeMapTrainPrediction,
    RealTimeMapBus,
    GTFSBus,
)


class Client:
    def __init__(self, api_key: str):
        self._gtfs_client = objectrest.RequestHandler(
            base_url="https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService",
        )
        self._legacy_client = objectrest.ApiTokenRequestHandler(
            base_url="http://developer.itsmarta.com",
            api_token=api_key,
            api_token_keyword="apiKey",
        )
        self._real_time_rail_client = objectrest.ApiTokenRequestHandler(
            base_url="https://developerservices.itsmarta.com:18096",
            api_token=api_key,
            api_token_keyword="apiKey",
        )
        self._lab_client = objectrest.ApiTokenRequestHandler(
            base_url="http://labs.itsmarta.com",
            api_token=api_key,
            api_token_keyword="api_key",
        )

    def _get_map_train_predictions(self) -> List[RealTimeMapTrainPrediction]:
        # noinspection PyTypeChecker
        return self._lab_client.get_object(
            url='/signpost/predictions',
            model=RealTimeMapTrainPrediction,
            extract_list=True,
        )

    def get_trains(self,
                   line: TrainLine = None,
                   station: str = None,
                   destination: str = None,
                   direction: Direction = None) -> List[LegacyTrain]:
        """
        Query API for train information

        :param line: Train line identifier filter (red, gold, green, or blue)
        :type line: str, optional
        :param station: train station filter
        :type station: str, optional
        :param destination: destination filter
        :type destination: Direction, optional
        :param direction: Direction train is heading
        :return: list of LegacyTrain objects
        :rtype: List[LegacyTrain]
        """
        # noinspection PyTypeChecker
        trains: List[LegacyTrain] = self._legacy_client.get_object(
            url='/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals',
            model=LegacyTrain,
            extract_list=True)

        filtered_trains: List[LegacyTrain] = []

        for train in trains:
            if line and train.line != line:
                continue
            if station and train.station != station:
                continue
            if destination and train.destination != destination:
                continue
            if direction and train.direction != direction:
                continue

            filtered_trains.append(train)

        return filtered_trains

    def get_real_time_trains(self,
                             line: TrainLine = None,
                             station: str = None,
                             destination: str = None,
                             direction: Direction = None) -> List[RealTimeTrain]:
        """
        Query API for train information

        :param line: Train line identifier filter (red, gold, green, or blue)
        :type line: str, optional
        :param station: train station filter
        :type station: str, optional
        :param destination: destination filter
        :type destination: Direction, optional
        :param direction: Direction train is heading
        :return: list of RealTimeTrain objects
        :rtype: List[RealTimeTrain]
        """
        # noinspection PyTypeChecker
        trains: List[RealTimeTrain] = self._real_time_rail_client.get_object(
            url='/railrealtimearrivals',
            model=RealTimeTrain,
            sub_keys=['RailArrivals'],
            extract_list=True,
        )

        filtered_trains: List[RealTimeTrain] = []

        for train in trains:
            if line and train.line != line:
                continue
            if station and train.station != station:
                continue
            if destination and train.destination != destination:
                continue
            if direction and train.direction != direction:
                continue

            filtered_trains.append(train)

        return filtered_trains

    def get_trains_from_map(self,
                            line: TrainLine = None,
                            station: str = None,
                            destination: str = None,
                            direction: Direction = None) -> List[RealTimeMapTrain]:
        """
        Query API for train information

        :param line: Train line identifier filter (red, gold, green, or blue)
        :type line: str, optional
        :param station: train station filter
        :type station: str, optional
        :param destination: destination filter
        :type destination: Direction, optional
        :param direction: Direction train is heading
        :return: list of RealTimeMapTrain objects
        :rtype: List[RealTimeMapTrain]
        """
        # noinspection PyTypeChecker
        trains: List[RealTimeMapTrain] = self._lab_client.get_object(
            url='/signpost/trains',
            model=RealTimeMapTrain,
            extract_list=True,
        )

        # I hate this loop. Why is this two separate endpoints, MARTA?
        train_predictions: List[RealTimeMapTrainPrediction] = self._get_map_train_predictions()
        for train in trains:
            for prediction in train_predictions:
                if prediction._match_for_map_train(map_train=train):
                    train.prediction = prediction

        filtered_trains: List[RealTimeMapTrain] = []

        for train in trains:
            if line and train.line != line:
                continue
            if station and train.prediction and train.prediction.station != station:
                continue
            if destination and train.destination != destination:
                continue
            if direction and train.direction != direction:
                continue

            filtered_trains.append(train)

        return filtered_trains

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
