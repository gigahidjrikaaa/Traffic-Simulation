import pytest
from trafficSim.simulation import Simulation


class TestSimulation:
    def test_simulation_initialization(self):
        sim = Simulation()
        assert sim.t == 0
        assert sim.frame_count == 0
        assert sim.dt == 1 / 60
        assert len(sim.roads) == 0
        assert len(sim.generators) == 0
        assert len(sim.traffic_signals) == 0
        assert sim.iteration == 0

    def test_create_road(self):
        sim = Simulation()
        road = sim.create_road((0, 0), (100, 0))

        assert len(sim.roads) == 1
        assert road in sim.roads

    def test_create_multiple_roads(self):
        sim = Simulation()
        sim.create_roads([
            ((0, 0), (100, 0)),
            ((100, 0), (200, 0)),
            ((200, 0), (300, 0))
        ])

        assert len(sim.roads) == 3

    def test_create_generator(self):
        sim = Simulation()
        sim.create_roads([((0, 0), (100, 0))])
        gen = sim.create_gen({
            'vehicle_rate': 10,
            'vehicles': [[1, {'path': [0]}]]
        })

        assert len(sim.generators) == 1
        assert gen in sim.generators
        assert sim.vehicle_rate == 10

    def test_create_signal(self):
        sim = Simulation()
        sim.create_roads([((0, 0), (100, 0)), ((100, 0), (200, 0))])

        signal = sim.create_signal([[0], [1]])

        assert len(sim.traffic_signals) == 1
        assert signal in sim.traffic_signals

    def test_run_single_step(self):
        sim = Simulation()
        sim.create_roads([((0, 0), (100, 0))])

        sim.run(1)

        assert sim.t > 0
        assert sim.frame_count == 1

    def test_run_multiple_steps(self):
        sim = Simulation()
        sim.create_roads([((0, 0), (100, 0))])

        sim.run(10)

        assert sim.t > 0
        assert sim.frame_count == 10

    def test_pause_and_resume(self):
        sim = Simulation()
        assert sim.is_paused is False

        sim.pause()
        assert sim.is_paused is True

        sim.resume()
        assert sim.is_paused is False

    def test_update_increments_time(self):
        sim = Simulation()
        sim.create_roads([((0, 0), (100, 0))])
        initial_t = sim.t

        sim.update()

        assert sim.t > initial_t

    def test_config_override(self):
        sim = Simulation({'dt': 0.5, 'iteration': 5})

        assert sim.dt == 0.5
        assert sim.iteration == 5
