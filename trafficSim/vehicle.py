import numpy as np

# Define Colors as constants
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

class Vehicle:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):  
        vehicleTypes = ["car", "truck", "bus", "motorcycle"]  
        colors = [RED, GREEN, BLUE, ORANGE, YELLOW, CYAN, PURPLE]
        # self.vehicleType with the probability:
        # car: 0.2
        # truck: 0.05
        # bus: 0.05
        # motorcycle: 0.7
        self.vehicleType = np.random.choice(vehicleTypes, p=[0.3, 0.1, 0.1, 0.5])
        if(self.vehicleType == "car"):
            self.l = 3
            self.h = 2
            self.color = RED
            self.s0 = 3
            self.T = 1
            self.v_max = 20
            self.a_max = 5
            self.b_max = 10
        elif(self.vehicleType == "truck"):
            self.l = 5
            self.h = 3
            self.color = YELLOW
            self.s0 = 5
            self.T = 1
            self.v_max = 15
            self.a_max = 4
            self.b_max = 8
        elif(self.vehicleType == "bus"):
            self.l = 5
            self.h = 3
            self.color = BLUE
            self.s0 = 4
            self.T = 1
            self.v_max = 20
            self.a_max = 6
            self.b_max = 12
        elif(self.vehicleType == "motorcycle"):
            self.l = 2
            self.h = 1
            self.color = ORANGE
            self.s0 = 2
            self.T = 1
            self.v_max = 25
            self.a_max = 7
            self.b_max = 20

        self.path = []
        self.current_road_index = 0

        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False

    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)
        self._v_max = self.v_max

    def update(self, lead, dt):
        delta_a = 2
        # Update position and velocity
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.l
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(0, self.T*self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1-(self.v/self.v_max)**delta_a - alpha**2)

        if self.stopped: 
            self.a = -self.b_max*self.v/self.v_max
        
    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max
        

