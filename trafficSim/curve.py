from typing import List, Tuple

def curve_points(start: Tuple[float, float], end: Tuple[float, float], control: Tuple[float, float], resolution: int = 5) -> List[Tuple[float, float]]:
	if (start[0] - end[0])*(start[1] - end[1]) == 0:
		return [start, end]

	path: List[Tuple[float, float]] = []

	for i in range(resolution+1):
		t = i/resolution
		x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 *end[0]
		y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 *end[1]
		path.append((x, y))

	return path

def curve_road(start: Tuple[float, float], end: Tuple[float, float], control: Tuple[float, float], resolution: int = 15) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
	points = curve_points(start, end, control, resolution=resolution)
	return [(points[i-1], points[i]) for i in range(1, len(points))]

TURN_LEFT = 0
TURN_RIGHT = 1

def turn_road(start: Tuple[float, float], end: Tuple[float, float], turn_direction: int, resolution: int = 15) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
	x = min(start[0], end[0])
	y = min(start[1], end[1])

	if turn_direction == TURN_LEFT:
		control: Tuple[float, float] = (
			x - y + start[1],
			y - x + end[0]
		)
	else:
		control = (
			x - y + end[1],
			y - x + start[0]
		)

	return curve_road(start, end, control, resolution=resolution)

