# Traffic-Simulation

A traffic flow simulation using the Intelligent-Driver Model (IDM) implemented in Python with Pygame visualization.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Architecture](#architecture)

## Overview

This project simulates traffic flow at a four-way intersection using microscopic traffic models. Vehicles follow the Intelligent-Driver Model (IDM) to realistically accelerate, decelerate, and maintain safe following distances.

### Simulation Model

The Intelligent-Driver Model calculates vehicle acceleration based on:

- **Desired speed**: Vehicles prefer to drive at their maximum safe speed
- **Gap to lead vehicle**: Vehicles maintain a safe following distance
- **Speed difference**: Vehicles slow down when approaching slower vehicles

## Features

- Realistic vehicle physics using IDM
- Four vehicle types: cars, trucks, buses, motorcycles
- Traffic signal control with configurable timing
- Multi-lane intersection support (up to 3 lanes per direction)
- Real-time Pygame visualization
- Vehicle path following through complex intersections
- Configurable simulation parameters via YAML files
- Comprehensive test coverage

## Installation

### Prerequisites

- Python 3.11+
- pip (comes with Python)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Traffic-Simulation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install development dependencies (optional, for contributing):
```bash
pip install -r requirements-dev.txt
```

## Quick Start

### Running the Simulation

```bash
python main.py
```

The simulation window will open showing:
- Vehicles moving through the intersection
- Traffic signals changing state (green/red)
- Real-time statistics (vehicles passed, present, average throughput)

### Controls

- **Mouse wheel**: Zoom in/out
- **Mouse drag**: Pan the view
- **Left click + drag**: Move the view

## Configuration

Simulation behavior can be customized through YAML configuration files in the `config/` directory.

### Configuration Files

- `config/default.yaml` - Main simulation parameters
- `config/vehicles.yaml` - Vehicle type definitions

### Key Parameters

#### Simulation Parameters (default.yaml)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `simulation.dt` | 0.01667 | Simulation timestep (seconds) |
| `simulation.time_limit` | 300 | Auto-reset interval (seconds) |
| `simulation.fps` | 60 | Frames per second |

#### Traffic Signal Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `traffic_signal.cycle_length_min` | 20 | Minimum green light duration |
| `traffic_signal.cycle_length_max` | 40 | Maximum green light duration |
| `traffic_signal.slow_distance` | 50 | Distance where vehicles start slowing (meters) |
| `traffic_signal.slow_factor` | 0.4 | Speed reduction factor in slowing zone |
| `traffic_signal.stop_distance` | 12 | Distance where vehicles stop (meters) |

#### Vehicle Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `vehicle_generator.vehicle_rate` | 20 | Vehicles spawned per minute |

#### Intersection Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `intersection.road_turn_iterations` | 20 | Bezier curve resolution |
| `intersection.road_length` | 300 | Length of road segments (meters) |
| `intersection.node_a` | -2 | Offset for intersection geometry |
| `intersection.node_b` | 12 | Offset for intersection geometry |

### Modifying Configuration

1. Open the desired config file in `config/`
2. Modify the parameter values
3. Restart the simulation

Example: Change simulation speed to run 2x faster
```yaml
simulation:
  dt: 0.00833  # 1/120 FPS
  fps: 120
```

## Project Structure

```
Traffic-Simulation/
├── config/              # Configuration files (YAML)
│   ├── default.yaml    # Simulation parameters
│   └── vehicles.yaml   # Vehicle type definitions
├── trafficSim/          # Main simulation package
│   ├── __init__.py       # Public API exports
│   ├── simulation.py      # Core simulation orchestrator
│   ├── vehicle.py         # Vehicle physics (IDM model)
│   ├── road.py            # Road segment logic
│   ├── traffic_signal.py # Traffic light control
│   ├── vehicle_generator.py # Vehicle spawning
│   ├── window.py          # Pygame visualization
│   ├── curve.py           # Bezier curve utilities
│   ├── road_network.py     # Road network builder
│   ├── config.py          # Configuration base class
│   └── config_loader.py   # YAML config loader
├── tests/              # Test suite
│   ├── test_vehicle.py   # Vehicle physics tests
│   ├── test_road.py      # Road logic tests
│   └── test_simulation.py # Simulation orchestration tests
├── main.py              # Entry point, road definitions
├── requirements.txt      # Runtime dependencies
└── requirements-dev.txt # Development dependencies
└── pyproject.toml       # Project configuration (ruff, mypy, pytest)
```

See individual README files in each directory for detailed documentation.

## Development

### Setting Up Development Environment

```bash
# Clone and navigate to project
cd Traffic-Simulation

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### Code Quality Tools

The project uses:

- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checker
- **pytest**: Testing framework with coverage

#### Running Quality Checks

```bash
# Lint code
ruff check trafficSim/

# Format code
ruff format trafficSim/

# Type check
mypy trafficSim --ignore-missing-imports

# Run tests
pytest tests/ -v --cov=trafficSim
```

### Pre-commit Hooks

Consider setting up pre-commit hooks for automatic quality checks:
```bash
pip install pre-commit
pre-commit install --hook-type=pre-commit-hooks.ruff
pre-commit install --hook-type=pre-commit-hooks.ruff-format
pre-commit install --hook-type=pre-commit-hooks.mypy
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_vehicle.py -v

# Run tests with coverage
pytest tests/ --cov=trafficSim --cov-report=html
```

### Test Organization

- `test_vehicle.py`: Vehicle physics, IDM model, state management
- `test_road.py`: Road logic, traffic signals, vehicle-road interaction
- `test_simulation.py`: Simulation orchestration, time advancement, configuration

### Adding Tests

1. Create a new test file in `tests/` or add to an existing one
2. Import the necessary classes from `trafficSim`
3. Write test methods using pytest
4. Run tests to verify they pass

Example test:
```python
from trafficSim.vehicle import Vehicle
import pytest

def test_vehicle_initialization():
    v = Vehicle()
    assert v.x == 0
    assert 0 <= v.v <= v.v_max
```

## Architecture

### Core Components

1. **Simulation** (`simulation.py`): Main orchestrator
   - Manages time advancement
   - Coordinates roads, vehicles, signals, generators
   - Tracks statistics (vehicles passed, present, throughput)

2. **Vehicle** (`vehicle.py`): Intelligent-Driver Model implementation
   - Acceleration/braking based on gap to lead vehicle
   - Multiple vehicle types with different physical properties
   - Stop/slow controls for traffic signals

3. **Road** (`road.py`): Road segment management
   - Vehicle queue management
   - Traffic signal integration
   - Position and orientation calculations

4. **TrafficSignal** (`traffic_signal.py`): Traffic light control
   - Configurable cycle timing
   - Red/green state management
   - Slow/stop zone enforcement

5. **VehicleGenerator** (`vehicle_generator.py`): Vehicle spawning
   - Rate-controlled vehicle generation
   - Space checking before spawning
   - Multi-path support

6. **Window** (`window.py`): Pygame visualization
   - Real-time rendering of simulation
   - Interactive controls (zoom, pan)
   - Statistics display

7. **IntersectionBuilder** (`road_network.py`): Road network construction
   - Programmatic 4-way intersection generation
   - Multi-lane support
   - Configurable geometry parameters

8. **Configurable** (`config.py`): Configuration base class
   - Provides unified configuration pattern across all classes
   - Validation for configuration keys

9. **ConfigLoader** (`config_loader.py`): YAML configuration management
   - Loads and parses configuration files
   - Type-safe color parsing

### Design Patterns

- **Strategy Pattern**: `Configurable` base class eliminates code duplication
- **Factory Pattern**: `IntersectionBuilder` creates complex road networks
- **Data Classes**: `RoadSegment`, `RoadPath` for type safety
- **Observer Pattern**: Traffic signals observe and control vehicle flow

## Todo Items

See the original todo list in the project README for current improvement goals.

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure they pass
5. Run linter and type checker
6. Submit a pull request

## Acknowledgments

- Intelligent-Driver Model: Martin Treiber and Ansgar Helbing
- Pygame: Pygame development team
