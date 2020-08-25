class Interpolator():
    def __init__(self,interpolation_func = lambda x: x,keyframes = {},time = 1000, framerate = 100):
        self.interpolation_func = interpolation_func
        # keyframes are dictionaries with keys from 0 to 1 (normalized frames) 
        # with a data dict with values we want to interpolate with interpolate func
        self.keyframes = keyframes
        self.current_data = None
        self.current_tick = 0
        self.time = time
        self.tick_rate = time / 1000 / framerate
    def load_keyframes(self,keyframes):
        self.keyframes = keyframes
    def interpolate(self):
        while self.current_tick <= 1:
            # get last datapoint,
            # get next datapoint
            # interpolate between them with i_func
            self.current_tick += self.tick_rate
class AnimationTimeline():
    def __init__(self,speed=1,length=1*1000):
        self.speed = speed
        self.length = length

