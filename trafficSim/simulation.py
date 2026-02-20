from typing import List, Any, Dict
from copy import deepcopy
from trafficSim.road import Road
from trafficSim.vehicle_generator import VehicleGenerator
from trafficSim.traffic_signal import TrafficSignal
import csv

class Simulation:
    vehicles_passed = 0
    vehicles_present = 0
    vehicle_rate = 0
    is_paused = False

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        if config is None:
            config = {}
        self.set_default_config()

        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self) -> None:
        self.t = 0.0
        self.frame_count = 0
        self.dt = 1 / 60
        self.roads: List[Road] = []
        self.generators: List[VehicleGenerator] = []
        self.traffic_signals: List[TrafficSignal] = []
        self.iteration = 0
        self.time_limit = 300

    def create_road(self, start: tuple, end: tuple) -> Road:
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list: List[Any]) -> None:
        for road in road_list:
            self.create_road(*road)

    def create_gen(self, config: Dict[str, Any] | None = None) -> VehicleGenerator:
        if config is None:
            config = {}
        gen = VehicleGenerator(self, config)
        self.generators.append(gen)
        Simulation.vehicle_rate = gen.vehicle_rate
        return gen

    def create_signal(self, roads: List[List[int]], config: Dict[str, Any] | None = None) -> TrafficSignal:
        if config is None:
            config = {}
        road_objects = [[self.roads[i] for i in road_group] for road_group in roads]
        sig = TrafficSignal(road_objects, config)
        self.traffic_signals.append(sig)
        return sig

    def update(self) -> None:
        for road in self.roads:
            road.update(self.dt)

        for gen in self.generators:
            gen.update()

        for signal in self.traffic_signals:
            signal.update(self)

        for road in self.roads:
            if len(road.vehicles) == 0:
                continue
            vehicle = road.vehicles[0]
            if vehicle.x >= road.length:
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    vehicle.current_road_index += 1
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(new_vehicle)
                else:
                    Simulation.vehicles_passed += 1
                road.vehicles.popleft()

        Simulation.vehicles_present = 0
        for road in self.roads:
            Simulation.vehicles_present += len(road.vehicles)

        self.t += self.dt
        self.frame_count += 1

        if self.t >= self.time_limit:
            print("Traffic Signal Cycle Length: " + str(self.traffic_signals[0].cycle_length))
            print("Time: " + str(self.t))
            print("Vehicles Passed: " + str(Simulation.vehicles_passed))
            print("Vehicles Present: " + str(Simulation.vehicles_present))
            print("Vehicle Rate: " + str(Simulation.vehicle_rate))
            print("Traffic Density: " + str(Simulation.vehicles_present / (len(self.roads) * self.roads[0].length)))
            print("Iteration: " + str(self.iteration))

            with open('data.csv', mode='a') as data_file:
                data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data_writer.writerow([self.traffic_signals[0].cycle_length, Simulation.vehicles_passed])

            self.t = 0.001
            for gen in self.generators:
                gen.delete_all_vehicles()
            Simulation.vehicles_passed = 0
            Simulation.vehicles_present = 0
            self.iteration += 1
            if self.iteration % 5 == 0:
                for signal in self.traffic_signals:
                    signal.cycle_length += 1

    def run(self, steps: int) -> None:
        for _ in range(steps):
            self.update()

    def pause(self) -> None:
        self.is_paused = True

    def resume(self) -> None:
        self.is_paused = False
