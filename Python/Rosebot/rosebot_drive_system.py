import motor

class DriveSystem:

    def __init__(self):
        self.car = motor.OrdinaryCar()

    def go(self, left_wheel_speed, right_wheel_speed):
        """ Speeds as integers from -100 to 100. """
        pass

    def stop(self):
        pass
