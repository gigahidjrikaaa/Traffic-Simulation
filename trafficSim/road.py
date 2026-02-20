from scipy.spatial import distance
from collections import deque
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from trafficSim.vehicle import Vehicle
    from trafficSim.traffic_signal import TrafficSignal

class Road:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start: tuple = start
        self.end: tuple = end

        self.vehicles: deque[Vehicle] = deque()

        self.init_properties()

    def init_properties(self) -> None:
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1] - self.start[1]) / self.length
        self.angle_cos = (self.end[0] - self.start[0]) / self.length
        self.has_traffic_signal = False

    def set_traffic_signal(self, signal: 'TrafficSignal', group: int) -> None:
        self.traffic_signal = signal
        self.traffic_signal_group = group
        self.has_traffic_signal = True

    @property
    def traffic_signal_state(self) -> bool:
        if self.has_traffic_signal:
            i = self.traffic_signal_group
            return bool(self.traffic_signal.current_cycle[i])
        return True

    def update(self, dt: float) -> None:
        n = len(self.vehicles)

        if n > 0:
            self.vehicles[0].update(None, dt)
            for i in range(1, n):
                lead = self.vehicles[i - 1]
                self.vehicles[i].update(lead, dt)

            if self.traffic_signal_state:
                self.vehicles[0].unstop()
                for vehicle in self.vehicles:
                    vehicle.unslow()
            else:
                if self.vehicles[0].x >= self.length - self.traffic_signal.slow_distance:
                    self.vehicles[0].slow(self.traffic_signal.slow_factor * self.vehicles[0]._v_max)
                if (self.vehicles[0].x >= self.length - self.traffic_signal.stop_distance and
                    self.vehicles[0].x <= self.length - self.traffic_signal.stop_distance / 2):
                    self.vehicles[0].stop()
