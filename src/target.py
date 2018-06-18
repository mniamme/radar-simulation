import time
import colors
class Target:
    angle = -1
    distance = -1
    time = -1.0
    color = ()
    # initalization
    def __init__(self, angle, distance):
        self.angle = angle
        self.distance = distance
        self.time = time.time()
        self.color = colors.red
        
