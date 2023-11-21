import board
import analogio
import pwmio
import time
import digitalio

class motor:
    def __init__(self,PWM_PIN,DIR_PIN,FREQ=1600,REVERSE=False):
        self.pwm = pwmio.PWMOut(PWM_PIN, frequency=FREQ)
        self.dir = digitalio.DigitalInOut(DIR_PIN)
        self.dir.direction = digitalio.Direction.OUTPUT
        if not REVERSE:
            self.forwards = True
            self.backwards = False
        else:
            self.forward = False
            self.backwards = True
    def drive(self,THROTTLE):
        max_pwm = 65535
        if THROTTLE == 0:
            self.pwm.duty_cycle = 0
            self.dir.value = False
            print("STOP")
            return
        if THROTTLE > 0:
            direction = self.forwards
        else:
            direction = self.backwards

        PWM_VALUE = int( abs(THROTTLE) * max_pwm )

        if PWM_VALUE > max_pwm:
            PWM_VALUE = max_pwm
        if PWM_VALUE < 0:
            PWM_VALUE = 0

        print(PWM_VALUE,direction)
        self.pwm.duty_cycle = PWM_VALUE
        self.dir.value = direction

