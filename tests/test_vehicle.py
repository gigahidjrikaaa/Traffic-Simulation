import pytest
from trafficSim.vehicle import Vehicle


class TestVehicle:
    def test_vehicle_initialization(self):
        v = Vehicle()
        assert v.x == 0
        assert 0 <= v.v <= v.v_max
        assert v.l > 0
        assert v.h > 0
        assert v.a == 0
        assert v.stopped is False
        assert v.path == []
        assert v.current_road_index == 0

    def test_vehicle_types(self):
        for _ in range(20):
            v = Vehicle()
            assert v.vehicle_type in ["car", "truck", "bus", "motorcycle"]

    def test_car_properties(self):
        v = Vehicle({"vehicle_type": "car"})
        assert v.vehicle_type == "car"
        assert v.l == 3
        assert v.h == 2
        assert v.v_max == 20
        assert v.a_max == 5
        assert v.b_max == 10

    def test_truck_properties(self):
        v = Vehicle({"vehicle_type": "truck"})
        assert v.vehicle_type == "truck"
        assert v.l == 5
        assert v.h == 3
        assert v.v_max == 15
        assert v.a_max == 4
        assert v.b_max == 8

    def test_bus_properties(self):
        v = Vehicle({"vehicle_type": "bus"})
        assert v.vehicle_type == "bus"
        assert v.l == 5
        assert v.h == 3
        assert v.v_max == 20
        assert v.a_max == 6
        assert v.b_max == 12

    def test_motorcycle_properties(self):
        v = Vehicle({"vehicle_type": "motorcycle"})
        assert v.vehicle_type == "motorcycle"
        assert v.l == 2
        assert v.h == 1
        assert v.v_max == 25
        assert v.a_max == 7
        assert v.b_max == 20

    def test_stop_and_unstop(self):
        v = Vehicle()
        v.stop()
        assert v.stopped is True

        v.unstop()
        assert v.stopped is False

    def test_slow_and_unslow(self):
        v = Vehicle()
        original_v_max = v._v_max
        v.slow(10)
        assert v.v_max == 10

        v.unslow()
        assert v.v_max == original_v_max

    def test_update_no_lead(self):
        v = Vehicle({"vehicle_type": "car"})
        initial_x = v.x
        initial_v = v.v

        v.update(None, 1.0)

        assert v.x >= initial_x
        assert 0 <= v.v <= v.v_max

    def test_update_with_lead(self):
        lead = Vehicle({"vehicle_type": "car"})
        lead.x = 50
        lead.v = 10

        follower = Vehicle({"vehicle_type": "car"})
        follower.x = 20
        follower.v = 15

        follower.update(lead, 1.0)

        assert follower.x > 20
        assert follower.v >= 0

    def test_update_negative_velocity(self):
        v = Vehicle({"vehicle_type": "car"})
        v.v = 10
        v.a = -20

        v.update(None, 1.0)

        assert v.v == 0
        assert v.x >= 0
