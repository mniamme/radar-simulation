import time
import colors
class Target:
    angle = -1
    time = -1.0
    color = ()
    # initalization
    def __init__(self, angle):
        self.angle = angle
        self.time = time.time()
        self.color = colors.red
