# Tests Directory

Test suite for the Traffic-Simulation project using pytest with coverage reporting.

## Table of Contents

- [Running Tests](#running-tests)
- [Test Organization](#test-organization)
- [Adding Tests](#adding-tests)
- [Coverage](#coverage)
- [Debugging Tests](#debugging-tests)

## Running Tests

### Quick Start

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=trafficSim --cov-report=html

# Run specific test file
pytest tests/test_vehicle.py -v

# Run specific test with verbose output
pytest tests/test_vehicle.py::test_vehicle_initialization -vv
```

### Continuous Testing During Development

To run tests automatically when files change:

```bash
# Install pytest-watch (if not already installed)
pip install pytest-watch

# Run tests in watch mode
pytest-watch tests/
```

### Filtering Tests

Run only tests matching a pattern:

```bash
# Only run vehicle tests
pytest tests/ -k vehicle

# Only run failing tests
pytest tests/ --lf

# Only run tests related to configuration
pytest tests/ -k config
```

### Test Output

Successful run:
```
============================= test session starts =============================
platform linux -- Python 3.11.9, pytest-9.0.2, pluggy-1.6.0
collected 31 items

tests/test_vehicle.py::TestVehicle::test_vehicle_initialization PASSED    [ 10%]
tests/test_vehicle.py::TestVehicle::test_vehicle_types PASSED              [ 20%]
...

=========================== short test summary info =============================
PASSED 31 in 3.45s ===============================
```

Coverage summary:
```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
trafficSim\__init__.py                8      0   100%
trafficSim\config.py                 14      2    86%
trafficSim\vehicle.py                62      1    98%
trafficSim\simulation.py             96     32    67%
trafficSim\traffic_signal.py         34      9    74%
trafficSim\vehicle_generator.py      37     12    68%
```

## Test Organization

### test_vehicle.py

Tests the Vehicle class and Intelligent-Driver Model implementation.

**Test Categories:**

1. **Initialization Tests**
   - `test_vehicle_initialization`: Vehicle starts with correct default values
   - `test_vehicle_types`: Vehicle type is one of the four supported types

2. **Property Tests**
   - `test_car_properties`: Car has correct default properties
   - `test_truck_properties`: Truck has correct default properties
   - `test_bus_properties`: Bus has correct default properties
   - `test_motorcycle_properties`: Motorcycle has correct default properties

3. **Physics Tests**
   - `test_stop_and_unstop`: Vehicle stop state management
   - `test_slow_and_unslow`: Vehicle speed limiting
   - `test_update_no_lead`: Vehicle accelerates correctly when no lead
   - `test_update_with_lead`: Vehicle follows lead vehicle
   - `test_update_negative_velocity`: Vehicle handles negative velocity correctly

### test_road.py

Tests the Road class and traffic signal integration.

**Test Categories:**

1. **Initialization Tests**
   - `test_road_initialization`: Road creates with correct geometry
   - `test_road_diagonal`: Diagonal road has correct angle calculations
   - `test_road_vertical`: Vertical road has correct orientation

2. **Signal Integration Tests**
   - `test_set_traffic_signal`: Traffic signal attachment
   - `test_traffic_signal_state_no_signal`: No signal defaults to green
   - `test_traffic_signal_green`: Green signal allows vehicle movement

3. **Vehicle Management Tests**
   - `test_add_vehicle`: Vehicle can be added to empty road
   - `test_update_no_vehicles`: Empty road handles update correctly
   - `test_update_single_vehicle`: Single vehicle updates correctly
   - `test_update_two_vehicles`: Two vehicles maintain following distance

### test_simulation.py

Tests the Simulation class and overall orchestration.

**Test Categories:**

1. **Setup Tests**
   - `test_simulation_initialization`: Simulation creates with correct defaults
   - `test_create_road`: Road creation works
   - `test_create_multiple_roads`: Multiple roads can be added
   - `test_create_generator`: Vehicle generator creation
   - `test_create_signal`: Traffic signal creation
   - `test_run_single_step`: Simulation advances correctly in one step
   - `test_run_multiple_steps`: Simulation advances over multiple steps
   - `test_pause_and_resume`: Simulation pause state management
   `test_update_increments_time`: Time advances correctly each update
   - `test_config_override`: Configuration override works

## Adding Tests

### Test Structure

```python
import pytest
from trafficSim import Vehicle, Simulation

class TestNewFeature:
    def test_new_feature():
        """
        Test description explaining what's being tested.
        """
        # Arrange
        sim = Simulation()
        vehicle = Vehicle()

        # Act
        result = vehicle.some_operation()

        # Assert
        assert result is expected
```

### Best Practices

1. **Arrange-Act-Assert Pattern**: Structure tests for clarity

2. **Descriptive Names**: Test names should describe what they test

3. **Independent Tests**: Each test should run in isolation

4. **Fixtures**: Use pytest fixtures for common setup:
```python
@pytest.fixture
def simulation():
    return Simulation()

@pytest.fixture
def car():
    return Vehicle({'vehicle_type': 'car'})
```

5. **Parameterized Tests**: Use pytest.mark.parametrize for testing multiple cases:
```python
@pytest.mark.parametrize('vehicle_type', ['car', 'truck', 'bus', 'motorcycle'])
def test_vehicle_properties(vehicle_type):
    v = Vehicle({'vehicle_type': vehicle_type})
    assert v.l > 0
    assert v.v_max > 0
```

6. **Mock External Dependencies**: For tests involving file I/O or slow operations:
```python
from unittest.mock import patch

def test_file_loading():
    with patch('trafficSim.config_loader.ConfigLoader.load_yaml') as mock_load:
        mock_load.return_value = {}
        from trafficSim.config_loader import ConfigLoader
        result = ConfigLoader.load_yaml('test.yaml')
        assert result == {}
```

## Coverage Goals

Aim for high coverage across all modules:

- **Minimum Coverage Target**: 70%
- **Current Coverage**: 46% (as of latest run)
- **Priority Modules for Improvement**:
  1. `simulation.py` - 67% coverage (32 missing statements)
   2. `vehicle.py` - 98% coverage (1 missing statement)
  3. `vehicle_generator.py` - 68% coverage (12 missing statements)
 4. `traffic_signal.py` - 74% coverage (9 missing statements)
 5. `road_network.py` - 0% coverage (new file)
 6. `window.py` - 15% coverage (visualization complex, hard to test)

## Known Test Limitations

### IDM Model Testing

The Intelligent-Driver Model is a deterministic mathematical model given specific inputs. Testing focuses on:

- **Correct parameter propagation**: Ensure configuration values are properly applied
- **Boundary conditions**: Edge cases (zero velocity, max velocity, negative gaps)
- **Type safety**: All vehicle properties are correct types

### Limitations:

- Does not test for numerical precision of IDM equations
- Does not test for complex multi-vehicle scenarios
- Does not test visualization (window.py)

### Testing Edge Cases

Critical edge cases to test:

1. **Zero gap**: Vehicle immediately behind another
2. **Large gap**: Maximum following distance
3. **High speed differential**: Fast vehicle approaching slow lead
4. **Red light with close following distance**: Should stop safely
5. **Green light transition**: Vehicles should accelerate from stop smoothly

```python
def test_red_light_close_following():
    v = Vehicle({'vehicle_type': 'car'})
    lead = Vehicle()
    lead.x = 10
    v.x = 5

    # Set road to red
    sim = Simulation()
    road = sim.create_roads([((0, 0), (100, 0)])[0]
    road.set_traffic_signal(
        TrafficSignal([[road]], 
        {'cycle': [(True, False, False, False)]})
    )

    # Vehicles should maintain safe distance
    assert lead.v < 5
    assert v.x < lead.x - v.s0 - lead.l
```

## Testing Configuration

Test that configuration changes take effect:

```python
def test_configuration_override():
    sim = Simulation({'dt': 0.03333})  # 2x speed

    sim.run(100)

    # Should process 3.3 seconds of simulation time
    assert abs(sim.t - 3.333) < 0.1  # Small tolerance
```

## Debugging Tests

### Using pytest Debuger

```bash
# Run with pdb for detailed debugging
pytest --pdb tests/test_vehicle.py::test_vehicle_initialization

# Run with ipdb (improved pdb)
pytest --ipdb tests/test_vehicle.py::test_vehicle_initialization
```

### Common Debugging Commands

```bash
# Run with verbose output and stop on first failure
pytest -x tests/

# Run specific test with maximum verbosity
pytest -vv -s tests/test_vehicle.py::test_vehicle_initialization

# List all available tests
pytest --collect-only tests/ --co
```

### Writing Good Tests

**DO:**

- **Write atomic tests** - Each test should test ONE thing
- **Use descriptive assertions** - `assert expected == actual, not just check truthiness`
- **Avoid testing implementation details** - Test behavior, not internal methods
- **Mock expensive operations** - File I/O, Pygame rendering

**DON'T:**

- **Test private methods** - Only test the public API
- **Test specific numbers** - Use constants or calculated values
- **Assert exact types** - Check isinstance(), not truthy values
- **Create complex fixtures** - Keep setup simple

### Testing Configuration Files

Test that configuration files load correctly:

```python
def test_default_config_loads():
    from trafficSim.config_loader import ConfigLoader

    default_config = ConfigLoader.get_default_config()
    assert 'simulation' in default_config
    assert 'traffic_signal' in default_config

def test_vehicles_config_loads():
    from trafficSim.config_loader import ConfigLoader

    vehicles_config = ConfigLoader.get_vehicles_config()
    assert 'vehicle_types' in vehicles_config
    for vehicle_type in ['car', 'truck', 'bus', 'motorcycle']:
        assert vehicle_type in vehicles_config['vehicle_types']
        config = vehicles_config['vehicle_types'][vehicle_type]
        assert 'v_max' in config
        assert 'l' in config
```

### Testing Color Parsing

```python
from trafficSim.config_loader import ConfigLoader

def test_color_parsing():
    # Valid colors
    assert ConfigLoader.parse_color([255, 0, 0]) == (255, 0, 0)
    assert ConfigLoader.parse_color([128, 128, 128]) == (128, 128, 128)

    # Invalid colors (too few elements)
    with pytest.raises(ValueError):
        ConfigLoader.parse_color([255, 0])  # Should raise

    # Invalid colors (too many elements)
    with pytest.raises(ValueError):
        ConfigLoader.parse_color([255, 0, 0, 0])  # Should raise
```

## Continuous Integration

### Running Tests as Part of Development Workflow

1. Make your code changes
2. Run relevant tests
3. Fix any failing tests
4. Run all tests to ensure no regressions
5. Run type checker: `mypy trafficSim --ignore-missing-imports`
6. Run linter: `ruff check trafficSim`
7. Commit changes

### Test Data

Create test data files in `tests/fixtures/` for complex scenarios:

```python
# tests/fixtures/intersection_configs.yaml
simple_4way_intersection_3lanes:
  road_turn_iterations: 20
  road_length: 300
  node_a: -2
  node_b: 12
  num_lanes: 3
```

Then load fixture in tests:
```python
import yaml
from pathlib import Path

@pytest.fixture
def simple_intersection_config():
    config_path = Path(__file__).parent / 'fixtures' / 'intersection_configs.yaml'
    with open(config_path) as f:
        return yaml.safe_load(f)
```

## Performance Testing

For performance-sensitive changes (e.g., optimization), use pytest-benchmark:

```bash
pip install pytest-benchmark

pytest-benchmark tests/test_vehicle.py::test_update_no_lead -k 'medium'
```

## Maintenance

### Updating Tests When Code Changes

1. **Adding a new feature**: Add comprehensive test coverage
2. **Fixing a bug**: Add regression tests
3. **Refactoring**: Ensure existing tests still pass
4. **Changing configuration**: Test new parameter values

### Removing Tests

Only remove tests for features that have been intentionally removed and confirmed deprecated.

## Test Drift Prevention

Run tests regularly to ensure code quality doesn't degrade:

```bash
# Add to pre-commit hook or CI
pip install pre-commit
pre-commit install --hook-type=pre-commit-hooks.pytest
pre-commit install --hook-type=pre-commit-hooks.pytest-cov

# Run pre-commit before commits
pre-commit run --files trafficSim/
```
