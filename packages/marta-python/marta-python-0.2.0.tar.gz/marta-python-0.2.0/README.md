# marta-python

Python library for accessing MARTA real-time API

## Installing

```
pip install marta-python
```

## Using

Declare a new instance of the MARTA `RailClient` or `BusClient` class:

```python
from marta import RailClient

rail_api = RailClient(api_key="MY_API_KEY")
```

There are methods available for accessing MARTA train and bus data, many of which accept optional parameters to filter the results.

```python
from marta import RailClient, BusClient, Direction, TrainLine

rail_api = RailClient(api_key="MY_API_KEY")
bus_api = BusClient(api_key="MY_API_KEY")

# Get all buses (via legacy API)
buses = bus_api.get_buses()

# Get buses by route
buses = bus_api.get_buses(route=1)

# Get buses by route and stop_id
buses = bus_api.get_buses(route=1, stop_id=900800)

# Get buses by route and vehicle_id
buses = bus_api.get_buses(route=1, vehicle_id=1405)

# Get buses by route and timepoint
buses = bus_api.get_buses(route=1, time_point="West End Station")

# Get buses by route, stop_id and vehicle_id
buses = bus_api.get_buses(route=1, stop_id=900800, vehicle_id=1405)

# Get all rail station arrivals
arrivals = rail_api.get_arrivals()

# Get trains by line, station and direction
arrivals = rail_api.get_arrivals().on_line(TrainLine.RED).arriving_at("FIVE POINTS STATION").heading(Direction.NORTH)
```

There are other train and bus methods available that utilize other MARTA APIs.

```python
from marta import BusClient, RailClient

bus_api = BusClient(api_key="MY_API_KEY")
rail_api = RailClient(api_key="MY_API_KEY")

# Get all bus locations (via GTFS API) (preferred)
bus_locations = bus_api.get_bus_locations_from_gtfs()

# Get all bus routes (via real-time map API)
bus_locations = bus_api.get_bus_locations_from_map()

# Get all trains (via real-time API)
trains = rail_api.get_real_time_trains()

# Get all trains (via secondary real-time map API)
trains = rail_api.get_trains_from_map()
```

Each method returns a list of objects that represent the trains or buses.