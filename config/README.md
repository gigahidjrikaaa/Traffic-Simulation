# Configuration Directory

This directory contains YAML configuration files for the Traffic-Simulation.

## Overview

The simulation uses YAML files to configure simulation parameters without requiring code changes. Configuration files are loaded at startup and validated for type safety.

## Configuration Files

### default.yaml

Main simulation parameters controlling the core simulation behavior.

| Section | Description |
|---------|-------------|
| `simulation` | Timestep, time limits, FPS settings |
| `traffic_signal` | Traffic light timing and behavior |
| `vehicle_generator` | Vehicle spawn rate |
| `intersection` | Road network geometry |

### vehicles.yaml

Vehicle type definitions including physical properties and spawn probabilities.

Each vehicle type defines:

- **probability**: Spawn probability weight (relative)
- **length**: Vehicle length in meters
- **height**: Vehicle height in meters
- **color**: Display color as RGB tuple [R, G, B]
- **s0**: Minimum following distance in IDM model
- **T**: Safe time headway in IDM model
- **v_max**: Maximum speed in m/s
- **a_max**: Maximum acceleration in m/s²
- **b_max**: Maximum braking in m/s²

## Parameter Descriptions

### Simulation Parameters

#### `simulation.dt` (default: 0.01667)

The simulation timestep in seconds. Smaller values provide more precise physics but require more computation.

**Effects:**
- Smaller: More accurate physics, slower simulation
- Larger: Faster simulation, less accurate physics

**Recommended values:**
- 0.01667 (60 FPS) - Balanced accuracy and speed
- 0.00833 (120 FPS) - Faster simulation
- 0.03333 (30 FPS) - Very fast simulation

#### `simulation.time_limit` (default: 300)

Simulation auto-reset interval in seconds. After this time, statistics are saved and the simulation resets.

**Purpose**: Prevent numerical drift in long-running simulations

#### `simulation.fps` (default: 60)

Target frames per second for the simulation loop. Higher values improve smoothness but require more computation.

### Traffic Signal Parameters

#### `traffic_signal.cycle_length_min` / `cycle_length_max` (default: 20, 40)

Random green light duration bounds. Each phase duration is randomly chosen within this range.

#### `traffic_signal.slow_distance` (default: 50)

Distance in meters from the stop line where vehicles begin slowing down. Vehicles entering this zone reduce speed.

#### `traffic_signal.slow_factor` (default: 0.4)

Speed multiplier applied in the slowing zone. Vehicles travel at `slow_factor * _v_max` in this zone.

#### `traffic_signal.stop_distance` (default: 12)

Distance in meters from the stop line where vehicles must come to a complete stop. Vehicles in this zone are stopped.

### Vehicle Generator Parameters

#### `vehicle_generator.vehicle_rate` (default: 20)

Number of vehicles spawned per minute across all generators.

**Note**: This is a global rate; all generators use the same spawn rate.

### Intersection Parameters

#### `intersection.road_turn_iterations` (default: 20)

Bezier curve resolution for turning roads. Higher values create smoother curves with more road segments.

**Trade-off**: More curves = more road objects = slower simulation

#### `intersection.road_length` (default: 300)

Length of each straight road segment in meters.

#### `intersection.node_a` / `node_b` (default: -2, 12)

Offset parameters for intersection geometry. These adjust the relative positioning of roads to create the intersection layout.

## Vehicle Type Configuration

### Pre-defined Types

#### Car
```yaml
car:
  probability: 0.3
  length: 3
  height: 2
  color: [255, 0, 0]
  s0: 3
  T: 1
  v_max: 20
  a_max: 5
  b_max: 10
```

**Characteristics**: Balanced vehicle with moderate performance

#### Truck
```yaml
truck:
  probability: 0.1
  length: 5
  height: 3
  color: [255, 255, 0]
  s0: 5
  T: 1
  v_max: 15
  a_max: 4
  b_max: 8
```

**Characteristics**: Large, slow, conservative acceleration and braking

#### Bus
```yaml
bus:
  probability: 0.1
  length: 5
  height: 3
  color: [0, 0, 255]
  s0: 4
  T: 1
  v_max: 20
  a_max: 6
   b_max: 12
```

**Characteristics**: Similar to truck with better acceleration

#### Motorcycle
```yaml
motorcycle:
  probability: 0.5
  length:  2
  height: 1
  color: [255, 165, 0]
  s0: 2
  T: 1
  v_max: 25
  a_max: 7
  b_max: 20
```

**Characteristics**: Fast, agile, hard braking

## Modifying Configuration

### Changing Simulation Speed

To make the simulation run 2x faster, double the FPS and halve the timestep:

```yaml
simulation:
  dt: 0.00833
  fps: 120
```

### Adjusting Traffic Signal Timing

To make traffic signals cycle faster with shorter green lights:

```yaml
traffic_signal:
  cycle_length_min: 10
  cycle_length_max: 20
```

### Adjusting Vehicle Spawn Rate

To double the traffic density:

```yaml
vehicle_generator:
  vehicle_rate: 40
```

### Adding New Vehicle Types

Add a new entry to `vehicles.yaml` with all required parameters:

```yaml
sports_car:
  probability: 0.08
  length: 4.5
  height: 2
  color: [255, 0, 0]
  s0: 3.5
  T: 1.2
  v_max: 30
  a_max: 8
  b_max: 15
```

### Parameter Tuning Guidelines

1. **Start conservative**: Begin with default values
2. **Change one parameter at a time**: Isolate the effect of each change
3. **Monitor with `win.zoom`**: Adjust zoom to see details
4. **Check statistics**: Verify throughput improvements with `vehicles_passed` / time

## Common Configuration Issues

### Vehicles Too Dense

**Symptoms**: Long queues, vehicles stopped frequently, low throughput

**Solutions**:
1. Reduce `vehicle_rate` in `vehicle_generator`
2. Increase `simulation.dt` slightly for more precise physics
3. Add more lanes in intersection

### Vehicles Too Sparse

**Symptoms**: No queues, intersection often empty, low throughput

**Solutions**:
1. Increase `vehicle_rate`
2. Decrease cycle times for traffic signals

### Vehicles Stopping Too Frequently

**Symptoms**: Vehicles stop at red lights and don't accelerate when green

**Solutions**:
1. Increase `traffic_signal.stop_distance` (more buffer)
2. Decrease `traffic_signal.slow_factor` (less aggressive slowing)
3. Decrease `vehicle_generator.vehicle_rate`

### Unrealistic Physics

**Symptoms**: Vehicles instant acceleration/deceleration, jerky movement

**Solutions**:
1. Decrease `simulation.dt` for more precise physics
2. Increase `traffic_signal.slow_distance` (more gradual slowing)
3. Decrease `vehicle.a_max` for all vehicle types

## Validation

Configuration files are validated on load:

- **Type checking**: Numeric parameters are validated to be correct types
- **Range checking**: Probabilities must be positive
- **Required fields**: All vehicle parameters are required
- **Color validation**: Colors must be 3-element tuples of integers 0-255

Invalid configurations will raise an `AttributeError` on startup with details of what's wrong.

## Advanced Configuration

### Custom Intersection Layout

The `IntersectionBuilder` can create non-standard intersections by modifying the geometry parameters:

```python
from trafficSim import Simulation, IntersectionBuilder

sim = Simulation()

# Wide intersection with short roads
builder = IntersectionBuilder(
    sim=sim,
    a=-4, b=20,    # Wider spacing
    length=200,         # Shorter roads
    n=15                # Fewer curve segments
)
)

roads = builder.build_four_way_intersection(num_lanes=2)
```

### Dynamic Vehicle Types at Runtime

You can create vehicles with custom configurations programmatically:

```python
from trafficSim.vehicle import Vehicle

# Create a faster car
fast_car = Vehicle({
    'v_max': 25,     # Override speed
    'a_max': 8,      # Override acceleration
    'path': [0, 1, 2]
})
```

This is useful for testing or implementing scenarios with specific vehicle types.

## Configuration File Priority

When multiple configuration files specify the same parameter:

1. **Programmatic overrides**: Values passed to class constructors have highest priority
2. **config/default.yaml**: Medium priority (default simulation config)
3. **config/vehicles.yaml**: Low priority (vehicle type definitions)

Example:
```python
# Vehicle with custom speed overrides both default and vehicle type
v = Vehicle({'v_max': 25})           # Highest priority
# Vehicle type config applies via set_defaults()    # Medium priority
# If both set, programmatic wins
```

## Debugging Configuration

To verify configuration is loaded correctly:

```python
from trafficSim.config_loader import ConfigLoader

# Load and print config
config = ConfigLoader.get_default_config()
print("Simulation config:", config)

# Load vehicle config
vehicles_config = ConfigLoader.get_vehicles_config()
print("Vehicle config:", vehicles_config)
```

## Related Documentation

- [Root README](../README.md) - Project overview and quick start
- [trafficSim/README.md](./trafficSim/README.md) - Module API documentation
- [tests/README.md](../tests/README.md) - Testing guide
- Main project README: [README.md](../README.md)
