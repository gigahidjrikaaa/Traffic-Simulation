import numpy as np
from trafficSim import *

sim = Simulation()

# Play with these
n = 15
a = -2
b = 12
l = 300

# Nodes
WEST_RIGHT_START = (-b-l, a)
WEST_LEFT_START =	(-b-l, -a)

SOUTH_RIGHT_START = (a, b+l)
SOUTH_LEFT_START = (-a, b+l)

EAST_RIGHT_START = (b+l, -a)
EAST_LEFT_START = (b+l, a)

NORTH_RIGHT_START = (-a, -b-l)
NORTH_LEFT_START = (a, -b-l)


WEST_RIGHT = (-b, a)
WEST_LEFT =	(-b, -a)

SOUTH_RIGHT = (a, b)
SOUTH_LEFT = (-a, b)

EAST_RIGHT = (b, -a)
EAST_LEFT = (b, a)

NORTH_RIGHT = (-a, -b)
NORTH_LEFT = (a, -b)

# Create Nodes with offset to avoid overlapping
WEST_RIGHT_START2 = (WEST_RIGHT_START[0], WEST_RIGHT_START[1] - 4)
WEST_LEFT_START2 = (WEST_LEFT_START[0], WEST_LEFT_START[1] + 4)

SOUTH_RIGHT_START2 = (SOUTH_RIGHT_START[0] - 4, SOUTH_RIGHT_START[1])
SOUTH_LEFT_START2 = (SOUTH_LEFT_START[0] + 4, SOUTH_LEFT_START[1])

EAST_RIGHT_START2 = (EAST_RIGHT_START[0], EAST_RIGHT_START[1] + 4)
EAST_LEFT_START2 = (EAST_LEFT_START[0], EAST_LEFT_START[1] - 4)

NORTH_RIGHT_START2 = (NORTH_RIGHT_START[0] + 4, NORTH_RIGHT_START[1])
NORTH_LEFT_START2 = (NORTH_LEFT_START[0] - 4, NORTH_LEFT_START[1])

# Create Nodes with offset to avoid overlapping
WEST_RIGHT2 = (WEST_RIGHT[0], WEST_RIGHT[1] - 4)
WEST_LEFT2 =	(WEST_LEFT[0], WEST_LEFT[1] + 4)

SOUTH_RIGHT2 = (SOUTH_RIGHT[0] - 4, SOUTH_RIGHT[1])
SOUTH_LEFT2 = (SOUTH_LEFT[0] + 4, SOUTH_LEFT[1])

EAST_RIGHT2 = (EAST_RIGHT[0], EAST_RIGHT[1] + 4)
EAST_LEFT2 = (EAST_LEFT[0], EAST_LEFT[1] - 4)

NORTH_RIGHT2 = (NORTH_RIGHT[0] + 4, NORTH_RIGHT[1])
NORTH_LEFT2 = (NORTH_LEFT[0] - 4, NORTH_LEFT[1])

# Roads
WEST_INBOUND = (WEST_RIGHT_START, WEST_RIGHT)
SOUTH_INBOUND = (SOUTH_RIGHT_START, SOUTH_RIGHT)
EAST_INBOUND = (EAST_RIGHT_START, EAST_RIGHT)
NORTH_INBOUND = (NORTH_RIGHT_START, NORTH_RIGHT)

WEST_OUTBOUND = (WEST_LEFT, WEST_LEFT_START)
SOUTH_OUTBOUND = (SOUTH_LEFT, SOUTH_LEFT_START)
EAST_OUTBOUND = (EAST_LEFT, EAST_LEFT_START)
NORTH_OUTBOUND = (NORTH_LEFT, NORTH_LEFT_START)

WEST_STRAIGHT = (WEST_RIGHT, EAST_LEFT)
SOUTH_STRAIGHT = (SOUTH_RIGHT, NORTH_LEFT)
EAST_STRAIGHT = (EAST_RIGHT, WEST_LEFT)
NORTH_STRAIGHT = (NORTH_RIGHT, SOUTH_LEFT)

WEST_RIGHT_TURN = turn_road(WEST_RIGHT, SOUTH_LEFT, TURN_RIGHT, n)
WEST_LEFT_TURN = turn_road(WEST_RIGHT, NORTH_LEFT, TURN_LEFT, n)

SOUTH_RIGHT_TURN = turn_road(SOUTH_RIGHT, EAST_LEFT, TURN_RIGHT, n)
SOUTH_LEFT_TURN = turn_road(SOUTH_RIGHT, WEST_LEFT, TURN_LEFT, n)

EAST_RIGHT_TURN = turn_road(EAST_RIGHT, NORTH_LEFT, TURN_RIGHT, n)
EAST_LEFT_TURN = turn_road(EAST_RIGHT, SOUTH_LEFT, TURN_LEFT, n)

NORTH_RIGHT_TURN = turn_road(NORTH_RIGHT, WEST_LEFT, TURN_RIGHT, n)
NORTH_LEFT_TURN = turn_road(NORTH_RIGHT, EAST_LEFT, TURN_LEFT, n)

# Create Roads
WEST_INBOUND2 = (WEST_RIGHT_START2, WEST_RIGHT2)
SOUTH_INBOUND2 = (SOUTH_RIGHT_START2, SOUTH_RIGHT2)
EAST_INBOUND2 = (EAST_RIGHT_START2, EAST_RIGHT2)
NORTH_INBOUND2 = (NORTH_RIGHT_START2, NORTH_RIGHT2)

WEST_OUTBOUND2 = (WEST_LEFT2, WEST_LEFT_START2)
SOUTH_OUTBOUND2 = (SOUTH_LEFT2, SOUTH_LEFT_START2)
EAST_OUTBOUND2 = (EAST_LEFT2, EAST_LEFT_START2)
NORTH_OUTBOUND2 = (NORTH_LEFT2, NORTH_LEFT_START2)

WEST_STRAIGHT2 = (WEST_RIGHT2, EAST_LEFT2)
SOUTH_STRAIGHT2 = (SOUTH_RIGHT2, NORTH_LEFT2)
EAST_STRAIGHT2 = (EAST_RIGHT2, WEST_LEFT2)
NORTH_STRAIGHT2 = (NORTH_RIGHT2, SOUTH_LEFT2)

WEST_RIGHT_TURN2 = turn_road(WEST_RIGHT2, SOUTH_LEFT2, TURN_RIGHT, n)
WEST_LEFT_TURN2 = turn_road(WEST_RIGHT2, NORTH_LEFT2, TURN_LEFT, n)

SOUTH_RIGHT_TURN2 = turn_road(SOUTH_RIGHT2, EAST_LEFT2, TURN_RIGHT, n)
SOUTH_LEFT_TURN2 = turn_road(SOUTH_RIGHT2, WEST_LEFT2, TURN_LEFT, n)

EAST_RIGHT_TURN2 = turn_road(EAST_RIGHT2, NORTH_LEFT2, TURN_RIGHT, n)
EAST_LEFT_TURN2 = turn_road(EAST_RIGHT2, SOUTH_LEFT2, TURN_LEFT, n)

NORTH_RIGHT_TURN2 = turn_road(NORTH_RIGHT2, WEST_LEFT2, TURN_RIGHT, n)
NORTH_LEFT_TURN2 = turn_road(NORTH_RIGHT2, EAST_LEFT2, TURN_LEFT, n)

sim.create_roads([
    WEST_INBOUND,   #0
    SOUTH_INBOUND,  #1
    EAST_INBOUND,   #2
    NORTH_INBOUND,  #3

    WEST_OUTBOUND,  #4
    SOUTH_OUTBOUND, #5
    EAST_OUTBOUND,  #6
    NORTH_OUTBOUND, #7

    WEST_STRAIGHT,  #8
    SOUTH_STRAIGHT, #9
    EAST_STRAIGHT,  #10
    NORTH_STRAIGHT, #11

    # NEW ROADS ----------------------------------------------
    WEST_INBOUND2,  #12
    SOUTH_INBOUND2, #13
    EAST_INBOUND2,  #14
    NORTH_INBOUND2, #15

    WEST_OUTBOUND2, #16
    SOUTH_OUTBOUND2, #17
    EAST_OUTBOUND2, #18
    NORTH_OUTBOUND2, #19

    WEST_STRAIGHT2, #20
    SOUTH_STRAIGHT2, #21
    EAST_STRAIGHT2, #22
    NORTH_STRAIGHT2, #23
    #----------------------------------------------------------------

    *WEST_RIGHT_TURN,
    *WEST_LEFT_TURN,

    *SOUTH_RIGHT_TURN,
    *SOUTH_LEFT_TURN,

    *EAST_RIGHT_TURN,
    *EAST_LEFT_TURN,

    *NORTH_RIGHT_TURN,
    *NORTH_LEFT_TURN,

    *WEST_RIGHT_TURN2,
    *WEST_LEFT_TURN2,
    
    *SOUTH_RIGHT_TURN2,
    *SOUTH_LEFT_TURN2,

    *EAST_RIGHT_TURN2,
    *EAST_LEFT_TURN2,

    *NORTH_RIGHT_TURN2,
    *NORTH_LEFT_TURN2
])

def road(a): return range(a, a+n)

sim.create_gen({
'vehicle_rate': 100,
'vehicles':[
    [3, {'path': [0, 8, 6]}],
    [2, {'path': [0, *road(24), 5]}],
    # [2, {'path': [0, *road(24+n), 7]}],

    [3, {'path': [1, 9, 7]}],
    [2, {'path': [1, *road(24+2*n), 6]}],
    # [1, {'path': [1, *road(24+3*n), 4]}],


    [3, {'path': [2, 10, 4]}],
    [2, {'path': [2, *road(24+4*n), 7]}],
    # [1, {'path': [2, *road(24+5*n), 5]}],

    [3, {'path': [3, 11, 5]}],
    [2, {'path': [3, *road(24+6*n), 4]}],
    # [2, {'path': [3, *road(24+7*n), 6]}],

    # '''NEW ROADS'''
    [3, {'path': [12, 20, 18]}],
    # [2, {'path': [12, *road(24+8*n), 17]}],
    [2, {'path': [12, *road(24+9*n), 19]}],

    [3, {'path': [13, 21, 19]}],
    # [2, {'path': [13, *road(24+10*n), 18]}],
    [1, {'path': [13, *road(24+11*n), 16]}],


    [3, {'path': [14, 22, 16]}],
    # [2, {'path': [14, *road(24+12*n), 19]}],
    [1, {'path': [14, *road(24+13*n), 17]}],

    [3, {'path': [15, 23, 17]}],
    # [2, {'path': [15, *road(24+14*n), 16]}],
    [2, {'path': [15, *road(24+15*n), 18]}]
]})

sim.create_signal([[0], [1], [2], [3]])
sim.create_signal([[12], [13], [14], [15]])


# Start simulation
win = Window(sim)
win.zoom = 10
win.run(steps_per_update=1)
