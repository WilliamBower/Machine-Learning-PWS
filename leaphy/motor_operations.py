from gpiozero import Motor

class Leaphy():
    def __init__(self):
        #define motor ports
        self.motorL = Motor(4, 14)
        self.motorR = Motor(17, 27)

        #define motor speeds
        self.LMax = 1 #max speed for straight line for left motor
        self.RMax = 1 #max speed for straight line for right motor
        
        self.LTurnL = self.LMax/2 #left turn left motor
        self.LTurnR = self.RMax #left turn right motor
        self.RTurnL = self.LMax #right turn left motor
        self.RTurnR = self.RMax/2 #right turn right motor

    def stop(self): 
        #stop all motors
        self.motorL.stop()
        self.motorR.stop()
    
    def straight(self, speed=1): 
        #go straight, at max speed with speed multiplier
        self.motorL.forward(self.LMax*speed)
        self.motorR.forward(self.RMax*speed)
    
    def l_turn(self, percentage=1, speed=1): 
        #turn left, sharper for a sharp turn with speed multiplier
        self.motorL.forward(self.LTurnL*percentage*speed)
        self.motorR.forward(self.LTurnR*percentage*speed)
    
    def r_turn(self, percentage=1, speed=1): 
        #turn right, sharper for a sharp turn with speed multiplier
        self.motorL.forward(self.RTurnL*percentage*speed)
        self.motorR.forward(self.RTurnR*percentage*speed)

leaphy = Leaphy()