import pytest
from collections import deque
from trafficSim.road import Road
from trafficSim.vehicle import Vehicle


class TestRoad:
    def test_road_initialization(self):
        road = Road((0, 0), (100, 0))
        assert road.start == (0, 0)
        assert road.end == (100, 0)
        assert road.length == 100
        assert isinstance(road.vehicles, deque)
        assert road.angle_sin == 0
        assert road.angle_cos == 1
        assert road.has_traffic_signal is False

    def test_road_diagonal(self):
        road = Road((0, 0), (100, 100))
        assert road.length > 0
        assert abs(road.angle_sin - 0.707) < 0.01
        assert abs(road.angle_cos - 0.707) < 0.01

    def test_road_vertical(self):
        road = Road((0, 0), (0, 100))
        assert road.length == 100
        assert road.angle_sin == 1
        assert road.angle_cos == 0

    def test_set_traffic_signal(self):
        road = Road((0, 0), (100, 0))
        from trafficSim.traffic_signal import TrafficSignal

        signal = TrafficSignal([[road]], {})
        road.set_traffic_signal(signal, 0)

        assert road.has_traffic_signal is True
        assert road.traffic_signal is signal
        assert road.traffic_signal_group == 0

    def test_traffic_signal_state_no_signal(self):
        road = Road((0, 0), (100, 0))
        assert road.traffic_signal_state is True

    def test_add_vehicle(self):
        road = Road((0, 0), (100, 0))
        vehicle = Vehicle()

        road.vehicles.append(vehicle)

        assert len(road.vehicles) == 1
        assert road.vehicles[0] == vehicle

    def test_update_no_vehicles(self):
        road = Road((0, 0), (100, 0))
        road.update(1.0)
        assert len(road.vehicles) == 0

    def test_update_single_vehicle(self):
        road = Road((0, 0), (100, 0))
        vehicle = Vehicle()
        vehicle.x = 0

        road.vehicles.append(vehicle)
        road.update(1.0)

        assert vehicle.x > 0

    def test_update_two_vehicles(self):
        road = Road((0, 0), (100, 0))
        lead = Vehicle()
        lead.x = 50

        follower = Vehicle()
        follower.x = 10

        road.vehicles.append(lead)
        road.vehicles.append(follower)

        road.update(1.0)

        assert lead.x > 50
        assert follower.x > 10

    def test_traffic_signal_green(self):
        road = Road((0, 0), (100, 0))
        from trafficSim.traffic_signal import TrafficSignal

        signal = TrafficSignal([[road]], {})
        signal.current_cycle_index = 3
        road.set_traffic_signal(signal, 0)

        vehicle = Vehicle()
        vehicle.x = 50
        road.vehicles.append(vehicle)

        road.update(1.0)

        assert vehicle.unslow is not None
