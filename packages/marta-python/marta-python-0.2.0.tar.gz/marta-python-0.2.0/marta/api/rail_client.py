from abc import ABC
from typing import List

from marta.api.client import Client
from marta.enums.direction import Direction
from marta.enums.train_line import TrainLine
from marta.models import (
    Arrival,
    Arrivals,
    RealTimeTrain,
    RealTimeMapTrain,
    RealTimeMapTrainPrediction,
)


class RailClient(Client, ABC):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def _get_map_train_predictions(self) -> List[RealTimeMapTrainPrediction]:
        # noinspection PyTypeChecker
        return self._lab_client.get_object(
            url='/signpost/predictions',
            model=RealTimeMapTrainPrediction,
            extract_list=True,
        )

    def get_arrivals(self) -> Arrivals:
        """
        Get all station arrivals

        :return: Arrivals object
        :rtype: Arrivals
        """
        # noinspection PyTypeChecker
        arrivals: List[Arrival] = self._legacy_client.get_object(
            url='/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals',
            model=Arrival,
            extract_list=True,
        )
        return Arrivals(arrivals=arrivals)

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
