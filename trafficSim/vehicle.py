import numpy as np
from typing import Optional, Any, Dict, List, Tuple
from trafficSim.config import Configurable
from trafficSim.config_loader import ConfigLoader

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

VEHICLE_TYPE_CONFIGS: Dict[str, Dict[str, Any]] = {
    "car": {"l": 3.0, "h": 2.0, "color": RED, "s0": 3.0, "T": 1.0, "v_max": 20.0, "a_max": 5.0, "b_max": 10.0},
    "truck": {"l": 5.0, "h": 3.0, "color": YELLOW, "s0": 5.0, "T": 1.0, "v_max": 15.0, "a_max": 4.0, "b_max": 8.0},
    "bus": {"l": 5.0, "h": 3.0, "color": BLUE, "s0": 4.0, "T": 1.0, "v_max": 20.0, "a_max": 6.0, "b_max": 12.0},
    "motorcycle": {"l": 2.0, "h": 1.0, "color": ORANGE, "s0": 2.0, "T": 1.0, "v_max": 25.0, "a_max": 7.0, "b_max": 20.0}
}

VEHICLE_TYPE_PROBABILITIES = [0.3, 0.1, 0.1, 0.5]
VEHICLE_TYPES = ["car", "truck", "bus", "motorcycle"]


class Vehicle(Configurable):
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.set_defaults()

        if config is not None:
            for attr, val in config.items():
                if hasattr(self, attr):
                    setattr(self, attr, val)

        self._apply_vehicle_type_properties()
        self.init_properties()

    def apply_config(self, config: Dict[str, Any]) -> None:
        Configurable.apply_config(self, config)
        self._apply_vehicle_type_properties()
        self.init_properties()

    def _apply_vehicle_type_properties(self) -> None:
        vehicle_type = getattr(self, 'vehicle_type', None)
        if vehicle_type and vehicle_type in VEHICLE_TYPE_CONFIGS:
            type_config = VEHICLE_TYPE_CONFIGS[vehicle_type]
            self.l = float(type_config["l"])
            self.h = float(type_config["h"])
            self.color = type_config["color"]
            self.s0 = float(type_config["s0"])
            self.T = float(type_config["T"])
            self.v_max = float(type_config["v_max"])
            self.a_max = float(type_config["a_max"])
            self.b_max = float(type_config["b_max"])

    def set_defaults(self) -> None:
        self.vehicle_type = np.random.choice(VEHICLE_TYPES, p=VEHICLE_TYPE_PROBABILITIES)
        config = VEHICLE_TYPE_CONFIGS[self.vehicle_type]

        self.l = float(config["l"])
        self.h = float(config["h"])
        self.color = config["color"]
        self.s0 = float(config["s0"])
        self.T = float(config["T"])
        self.v_max = float(config["v_max"])
        self.a_max = float(config["a_max"])
        self.b_max = float(config["b_max"])

        self.path: List[int] = []
        self.current_road_index = 0

        self.x = 0.0
        self.v = float(self.v_max)
        self.a = 0.0
        self.stopped = False
        self.time_added = 0.0

    def init_properties(self) -> None:
        self.sqrt_ab: float = 2 * np.sqrt(float(self.a_max) * float(self.b_max))
        self._v_max: float = float(self.v_max)

    def update(self, lead: Optional['Vehicle'], dt: float) -> None:
        delta_a = 2

        if self.v + self.a * dt < 0:
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0.0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt * dt / 2

        alpha = 0.0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T * self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1 - (self.v / self.v_max) ** delta_a - alpha ** 2)

        if self.stopped:
            self.a = -self.b_max * self.v / self.v_max

    def stop(self) -> None:
        self.stopped = True

    def unstop(self) -> None:
        self.stopped = False

    def slow(self, v: float) -> None:
        self.v_max = v

    def unslow(self) -> None:
        self.v_max = self._v_max


