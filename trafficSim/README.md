# trafficSim Module

The main simulation package implementing the Intelligent-Driver Model (IDM) for traffic flow simulation.

## Table of Contents

- [Module Overview](#module-overview)
- [Public API](#public-api)
- [Key Classes](#key-classes)
- [Usage Examples](#usage-examples)
- [Extending the Module](#extending-the-module)

## Module Overview

This module provides a complete traffic simulation system including:

- **Vehicle physics**: Realistic acceleration/braking using the Intelligent-Driver Model
- **Road management**: Road segments, vehicle queuing, traffic signal integration
- **Traffic signals**: Configurable timing and state management
- **Vehicle generation**: Rate-controlled spawning with path following
- **Visualization**: Real-time Pygame rendering
- **Configuration**: YAML-based configuration with validation
- **Network building**: Programmatic road network construction

The module is designed to be modular and extensible, with clear separation of concerns between physics, rendering, and logic.

## Public API

The `trafficSim` module exports the following public classes and functions:

### Classes

```python
from trafficSim import (
    Simulation,      # Main simulation orchestrator
    Vehicle,        # Vehicle with IDM physics
    Road,           # Road segment manager
    TrafficSignal,   # Traffic light controller
    VehicleGenerator, # Vehicle spawner
    Window,          # Pygame visualizer
    IntersectionBuilder, # Road network factory
)
    ConfigLoader,     # Configuration file loader
    Configurable,     # Configuration base class
)
)
```

### Functions

```python
from trafficSim import (
    turn_road,       # Create curved road segments
    curve_points,    # Calculate Bezier curve points
    curve_road,      # Generate road from curve points
    TURN_LEFT,       # Left turn direction constant
    TURN_RIGHT,      # Right turn direction constant
)
```

## Key Classes

### Simulation

**Purpose**: Main orchestrator that manages all simulation components.

**Key Methods**:
- `update()`: Advance simulation by one timestep
- `create_road(start, end)`: Add a road segment
- `create_roads(road_list)`: Add multiple road segments
- `create_gen(config)`: Create vehicle generator
- `create_signal(roads, config)`: Create traffic signal
- `run(steps)`: Run simulation for specified steps
- `pause()`, `resume()`: Control simulation execution

**Key Properties**:
- `t`: Current simulation time (seconds)
- `dt`: Timestep duration
- `vehicles_passed`: Total vehicles that exited the simulation
- `vehicles_present`: Current vehicles in the simulation
- `vehicle_rate`: Vehicles per minute spawn rate

### Vehicle

**Purpose**: Implements the Intelligent-Driver Model for realistic vehicle physics.

**Key Methods**:
- `update(lead, dt)`: Update vehicle state for timestep
- `stop()`, `unstop()`: Force vehicle to stop
- `slow(v)`, `unslow()`: Reduce maximum speed
- `init_properties()`: Calculate IDM parameters

**Key Properties**:
- `vehicle_type`: One of "car", "truck", "bus", "motorcycle"
- `l`, `h`: Vehicle dimensions (length, height in meters)
- `v_max`: Maximum speed (m/s)
- `a_max`, `b_max`: Maximum acceleration/braking (m/s²)
- `x`, `v`, `a`: Current position, velocity, acceleration
- `path`: List of road indices to follow
- `color`: Display color (RGB tuple)

**Supported Vehicle Types**:
| Type | Length | Height | Max Speed | Max Accel | Max Brake |
|------|--------|---------|---------|----------|---------|
| car | 3.0m | 2.0m | 20 m/s | 5 m/s² | 10 m/s² |
| truck | 5.0m | 3.0m | 15 m/s | 4 m/s² | 8 m/s² |
| bus | 5.0m | 3.0m | 20 m/s | 6 m/s² | 12 m/s² |
| motorcycle | 2.0m | 1.0m | 25 m/s | 7 m/s² | 20 m/s² |

### Road

**Purpose**: Manages a single road segment with vehicle queue and traffic signal integration.

**Key Methods**:
- `update(dt)`: Update all vehicles on this road
- `set_traffic_signal(signal, group)`: Attach traffic signal

**Key Properties**:
- `start`, `end`: Endpoint coordinates (x, y)
- `length`: Road segment length (meters)
- `angle_sin`, `angle_cos`: Road orientation
- `vehicles`: Deque of vehicles in order
- `has_traffic_signal`: Whether a traffic signal is attached
- `traffic_signal_state`: Current green/red state

### TrafficSignal

**Purpose**: Manages traffic light timing and state transitions.

**Key Methods**:
- `update(sim)`: Update signal state based on simulation time
- `current_cycle`: Tuple of current green/red states for each road group

**Key Configuration**:
- `cycle_length`: Duration of each green light phase
- `cycle_length_min`, `cycle_length_max`: Random bounds for cycle length
- `slow_distance`: Distance where vehicles begin slowing (meters)
- `slow_factor`: Speed reduction factor (0.0-1.0)
- `stop_distance`: Distance where vehicles must stop (meters)

### VehicleGenerator

**Purpose**: Spawns vehicles at configurable rate with path following.

**Key Methods**:
- `update()`: Attempt to spawn vehicles based on rate
- `delete_all_vehicles()`: Clear all vehicles from roads

**Key Configuration**:
- `vehicle_rate`: Vehicles per minute spawn rate
- `vehicles`: List of (weight, config) tuples defining spawn probabilities

### Window

**Purpose**: Pygame-based visualization of the simulation.

**Key Methods**:
- `run(steps_per_update)`: Run simulation loop with specified steps per frame
- `draw()`: Render the complete scene
- `draw_roads()`, `draw_vehicles()`, `draw_signals()`: Render specific elements
- `draw_status()`: Render statistics overlay

**Key Configuration**:
- `width`, `height`: Window dimensions (pixels)
- `fps`: Target frames per second
- `zoom`, `offset`: View transformation

### IntersectionBuilder

**Purpose**: Factory for building 4-way intersection road networks programmatically.

**Key Methods**:
- `build_four_way_intersection(num_lanes)`: Create complete intersection with configurable lanes

**Key Parameters**:
- `n`: Bezier curve resolution
- `length`: Road segment length
- `a`, `b`: Intersection geometry offset parameters

## Usage Examples

### Basic Simulation Setup

```python
from trafficSim import Simulation, IntersectionBuilder

# Create simulation
sim = Simulation({'dt': 0.016, 'fps': 60})

# Build intersection with 3 lanes
builder = IntersectionBuilder(sim, n=20, a=-2, b=12, length=300)
road_indices = builder.build_four_way_intersection(num_lanes=3)

# Create generator
gen = sim.create_gen({
    'vehicle_rate': 400,
    'vehicles': [
        [2, {'path': [road_indices[0], road_indices[4], road_indices[8]}],
        [1, {'path': [road_indices[1], road_indices[5], road_indices[9]}]
    ]
})

# Create traffic signals for each direction
sim.create_signal([[road_indices[0]], {})  # West
sim.create_signal([[road_indices[1]], {})  # South
sim.create_signal([[road_indices[2]], {})  # East
sim.create_signal([[road_indices[3]], {})  # North

# Run simulation
from trafficSim import Window
win = Window(sim)
win.run(steps_per_update=1)
```

### Custom Vehicle Configuration

```python
from trafficSim import Vehicle

# Create a custom vehicle type
v = Vehicle({
    'vehicle_type': 'car',
    'v_max': 15.0,  # Override default max speed
    'a_max': 3.0    # More gentle acceleration
    'path': [0, 1, 2]  # Custom path
})
```

### Using IntersectionBuilder

```python
from trafficSim import Simulation, IntersectionBuilder

sim = Simulation()

# Build compact 2-lane intersection
builder = IntersectionBuilder(sim, n=15, a=-2, b=10, length=200)
roads = builder.build_four_way_intersection(num_lanes=2)

print(f"Created {len(roads)} roads")
```

## Extending the Module

### Adding New Vehicle Types

1. Update `config/vehicles.yaml` with new vehicle definition
2. The vehicle will be automatically available in all Vehicle instances

Example:
```yaml
suv:
  probability: 0.15
  length: 5
  height: 2
  color: [128, 0, 128]  # Dark gray
  s0: 4
  T: 1.5
  v_max: 18
  a_max: 4
  b_max: 8
```

### Custom Road Logic

To add custom road behavior, subclass `Road` and override methods:

```python
from trafficSim.road import Road as BaseRoad

class CustomRoad(BaseRoad):
    def update(self, dt):
        # Custom update logic
        super().update(dt)
        # Your custom logic here
```

### Adding Visualization Elements

To add custom rendering to `Window`:

1. Add new method to Window class
2. Call it from `draw()` method
3. Ensure proper coordinate transformations using `self.convert()` and `self.inverse_convert()`

## Design Decisions

- **IDM Model Chosen**: Provides realistic car-following behavior with proven accuracy
- **YAML Configuration**: Allows parameter tuning without code changes
- **Separation of Concerns**: Physics, logic, and rendering are independent
- **Type Safety**: Full mypy coverage enables IDE support and early error detection
- **Test Coverage**: Comprehensive tests ensure reliability
- **Factory Pattern**: IntersectionBuilder simplifies complex road network creation

## Performance Considerations

- Use `numpy` operations for vector calculations
- Minimize object creation in tight loops (simulation update)
- Pygame rendering limited by `fps` target
- Use deque for vehicle queues for O(1) prepend/append

## Known Limitations

- Vehicles only follow pre-defined paths (no dynamic routing)
- No collision detection between vehicles (vehicles occupy different road queues)
- Traffic signals follow fixed cycle patterns (no adaptive timing)
- Simplified vehicle types (no lane changing, no overtaking)
- Pygame window required for visualization (no headless mode)
