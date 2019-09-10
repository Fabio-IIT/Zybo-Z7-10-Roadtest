import os
from uio import UIO
import struct 

PWM_CTRL_OFFSET = 0
PWM_PERIOD_OFFSET = 0x8
PWM_DUTY_OFFSET = 0x40

DEFAULT_PERIOD=60000
DEFAULT_DUTYCYCLE=30000

BLUE=0
GREEN=1
RED=2

class PWM_RGB(UIO):
    def __init__(self,uioNum,mapNum):
        super(PWM_RGB,self).__init__(uioNum,mapNum)

    def enable(self):
        self.mmap[PWM_CTRL_OFFSET:PWM_CTRL_OFFSET+1]=struct.pack('<B',1)

    def disable(self):
        self.mmap[PWM_CTRL_OFFSET:PWM_CTRL_OFFSET+1]=struct.pack('<B',0)

    def setDutyCycle(self,colour,duty):
        self.mmap[PWM_DUTY_OFFSET+4*colour:PWM_DUTY_OFFSET+4*(colour+1)]=struct.pack('<L',duty)

    def setPeriod(self,period):
        self.mmap[PWM_PERIOD_OFFSET:PWM_PERIOD_OFFSET+4]=struct.pack('<L',period)

    def getDutyCycle(self,colour):
        return struct.unpack('<L',self.mmap[PWM_DUTY_OFFSET+4*colour:PWM_DUTY_OFFSET+4*(colour+1)])

    def getPeriod(self,colour):
        return struct.unpack('<L',self.mmap[PWM_PERIOD_OFFSET:PWM_PERIOD_OFFSET+4])

    def close(self):
        self.release()

    def red(self):
        self.setDutyCycle(RED,DEFAULT_DUTYCYCLE)
        self.setDutyCycle(GREEN,0)
        self.setDutyCycle(BLUE,0)
    
    def green(self):
        self.setDutyCycle(GREEN,DEFAULT_DUTYCYCLE)
        self.setDutyCycle(RED,0)
        self.setDutyCycle(BLUE,0)

    def blue(self):
        self.setDutyCycle(BLUE,DEFAULT_DUTYCYCLE)
        self.setDutyCycle(GREEN,0)
        self.setDutyCycle(RED,0)


if __name__ == '__main__':
    import sys
    pwm=PWM_RGB(4,0)
    cmd = sys.argv[1]
    if cmd == 'off':
        pwm.disable()
    pwm.close()
