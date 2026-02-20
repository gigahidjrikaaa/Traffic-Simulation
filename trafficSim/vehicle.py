import numpy as np
from typing import Optional, Any, Dict, List, Tuple

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

class Vehicle:
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        if config is None:
            config = {}
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

        self._apply_vehicle_type_properties()
        self.init_properties()

    def set_default_config(self) -> None:
        vehicle_types = ["car", "truck", "bus", "motorcycle"]
        self.vehicle_type = np.random.choice(vehicle_types, p=[0.3, 0.1, 0.1, 0.5])

        self.l = 3
        self.h = 2
        self.color = RED
        self.s0 = 3.0
        self.T = 1.0
        self.v_max = 20.0
        self.a_max = 5.0
        self.b_max = 10.0

        self.path: List[int] = []
        self.current_road_index = 0

        self.x = 0.0
        self.v = float(self.v_max)
        self.a = 0.0
        self.stopped = False
        self.time_added = 0.0

    def _apply_vehicle_type_properties(self) -> None:
        if self.vehicle_type == "car":
            self.l = 3
            self.h = 2
            self.color = RED
            self.s0 = 3.0
            self.T = 1.0
            self.v_max = 20.0
            self.a_max = 5.0
            self.b_max = 10.0
        elif self.vehicle_type == "truck":
            self.l = 5
            self.h = 3
            self.color = YELLOW
            self.s0 = 5.0
            self.T = 1.0
            self.v_max = 15.0
            self.a_max = 4.0
            self.b_max = 8.0
        elif self.vehicle_type == "bus":
            self.l = 5
            self.h = 3
            self.color = BLUE
            self.s0 = 4.0
            self.T = 1.0
            self.v_max = 20.0
            self.a_max = 6.0
            self.b_max = 12.0
        elif self.vehicle_type == "motorcycle":
            self.l = 2
            self.h = 1
            self.color = ORANGE
            self.s0 = 2.0
            self.T = 1.0
            self.v_max = 25.0
            self.a_max = 7.0
            self.b_max = 20.0

    def init_properties(self) -> None:
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)
        self._v_max = float(self.v_max)

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


