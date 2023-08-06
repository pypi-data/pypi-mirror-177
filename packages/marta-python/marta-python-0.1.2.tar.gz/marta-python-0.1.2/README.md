# marta-python

Python library for accessing MARTA real-time API

## Installing

```
pip install marta-python
```

## Using

Declare a new instance of the MARTA `Client` class:

```python
from marta import Client

api = Client(api_key="MY_API_KEY")
```

There are methods available for accessing MARTA train and bus data, many of which accept optional parameters to filter the results.

```python
from marta import Client, Direction, TrainLine

api = Client(api_key="MY_API_KEY")

# Get all buses (via legacy API)
buses = api.get_buses()

# Get buses by route
buses = api.get_buses(route=1)

# Get buses by route and stop_id
buses = api.get_buses(route=1, stop_id=900800)

# Get buses by route and vehicle_id
buses = api.get_buses(route=1, vehicle_id=1405)

# Get buses by route and timepoint
buses = api.get_buses(route=1, time_point="West End Station")

# Get buses by route, stop_id and vehicle_id
buses = api.get_buses(route=1, stop_id=900800, vehicle_id=1405)

# Get all trains (via legacy API)
trains = api.get_trains()

# Get trains by line
trains = api.get_trains(line=TrainLine.RED)

# Get trains by station
trains = api.get_trains(station='Midtown Station')

# Get trains by destination
trains = api.get_trains(destination='Doraville')

# Get trains by line, station, and destination
trains = api.get_trains(line=TrainLine.BLUE, station='Five Points Station', destination='Indian Creek')

# Get trains by line, station, and direction
trains = api.get_trains(line=TrainLine.GOLD, station='Five Points Station', direction=Direction.NORTH)
```

There are other train and bus methods available that utilize other MARTA APIs.

```python
from marta import Client

api = Client(api_key="MY_API_KEY")

# Get all bus locations (via GTFS API) (preferred)
bus_locations = api.get_bus_locations_from_gtfs()

# Get all bus routes (via real-time map API)
bus_locations = api.get_bus_locations_from_map()

# Get all trains (via real-time API)
trains = api.get_real_time_trains()

# Get all trains (via secondary real-time map API)
trains = api.get_trains_from_map()
```

Each method returns a list of objects that represent the trains or buses.