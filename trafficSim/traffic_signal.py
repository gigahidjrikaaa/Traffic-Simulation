import random
from typing import List, Any, Dict, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from trafficSim.simulation import Simulation
    from trafficSim.road import Road

class TrafficSignal:
    def __init__(self, roads: List[List['Road']], config: Dict[str, Any] | None = None) -> None:
        if config is None:
            config = {}
        self.roads = roads
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

        self.init_properties()

    def set_default_config(self) -> None:
        self.cycle: List[Tuple[bool, bool, bool, bool]] = [
            (False, False, False, True),
            (False, False, True, False),
            (False, True, False, False),
            (True, False, False, False)
        ]
        self.slow_distance = 50
        self.slow_factor = 0.4
        self.stop_distance = 12
        self.cycle_length = 1

        self.current_cycle_index = 0
        self.last_t = 0

    def init_properties(self) -> None:
        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_signal(self, i)

    @property
    def current_cycle(self) -> Tuple[bool, bool, bool, bool]:
        return self.cycle[self.current_cycle_index]

    def update(self, sim: 'Simulation') -> None:
        cycle_length = self.cycle_length
        if sim.t % cycle_length == 0:
            cycle_length = random.randint(20, 40)
        k = (sim.t // cycle_length) % 4
        self.current_cycle_index = int(k)
        if len(self.roads) < 4:
            self.current_cycle_index = 3

