from dataclasses import dataclass
from typing import List, Tuple, Optional
from trafficSim.simulation import Simulation
from trafficSim.curve import turn_road, TURN_LEFT, TURN_RIGHT


@dataclass
class RoadSegment:
    """Represents a road segment between two points."""
    start: Tuple[float, float]
    end: Tuple[float, float]


@dataclass
class RoadPath:
    """Represents a path through multiple roads by index."""
    road_indices: List[int]
    probability: int = 1


class IntersectionBuilder:
    """Builds intersection road networks programmatically."""

    def __init__(self, sim: Simulation, n: int = 20, a: int = -2, b: int = 12, length: float = 300):
        """Initialize the intersection builder.

        Args:
            sim: The simulation instance
            n: Number of iterations for road turns
            a: Offset parameter for point a
            b: Offset parameter for point b
            length: Length of road segments
        """
        self.sim = sim
        self.n = n
        self.a = a
        self.b = b
        self.length = length

    def build_four_way_intersection(self, num_lanes: int = 3) -> List[int]:
        """Build a standard 4-way intersection with configurable lanes.

        Args:
            num_lanes: Number of lanes per direction

        Returns:
            List of road indices that were created
        """
        road_index = 0
        created_indices: List[int] = []

        for lane in range(num_lanes):
            lane_offset = lane * 4

            west_right_start = (-(self.b + self.length), self.a - lane_offset)
            west_left_start = (-(self.b + self.length), -self.a + lane_offset)

            south_right_start = (self.a - lane_offset, self.b + self.length)
            south_left_start = (-self.a + lane_offset, self.b + self.length)

            east_right_start = (self.b + self.length, -self.a + lane_offset)
            east_left_start = (self.b + self.length, self.a - lane_offset)

            north_right_start = (-self.a + lane_offset, -(self.b + self.length))
            north_left_start = (self.a - lane_offset, -(self.b + self.length))

            west_right = (-self.b, self.a - lane_offset)
            west_left = (-self.b, -self.a + lane_offset)

            south_right = (self.a - lane_offset, self.b)
            south_left = (-self.a + lane_offset, self.b)

            east_right = (self.b, -self.a + lane_offset)
            east_left = (self.b, self.a - lane_offset)

            north_right = (-self.a + lane_offset, -self.b)
            north_left = (self.a - lane_offset, -self.b)

            self._add_road(road_index, RoadSegment(west_right_start, west_right))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(south_right_start, south_right))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(east_right_start, east_right))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(north_right_start, north_right))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(west_left, west_left_start))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(south_left, south_left_start))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(east_left, east_left_start))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(north_left, north_left_start))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(west_right, east_left))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(south_right, north_left))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(east_right, west_left))
            created_indices.append(road_index)
            road_index += 1

            self._add_road(road_index, RoadSegment(north_right, south_left))
            created_indices.append(road_index)
            road_index += 1

            for turn_start, turn_end, turn_type in [
                (west_right, south_left, TURN_LEFT),
                (west_right, north_left, TURN_RIGHT),
                (south_right, east_left, TURN_LEFT),
                (south_right, west_left, TURN_RIGHT),
                (east_right, north_left, TURN_LEFT),
                (east_right, south_left, TURN_RIGHT),
                (north_right, west_left, TURN_LEFT),
                (north_right, east_left, TURN_RIGHT)
            ]:
                turn_roads = turn_road(turn_start, turn_end, turn_type, self.n)
                for road in turn_roads:
                    self._add_road(road_index, RoadSegment(*road))
                    created_indices.append(road_index)
                    road_index += 1

        return created_indices

    def _add_road(self, index: int, segment: RoadSegment) -> None:
        """Add a road to the simulation at the specified index.

        Args:
            index: The road index (must match current road count)
            segment: The road segment definition
        """
        self.sim.create_road(segment.start, segment.end)
