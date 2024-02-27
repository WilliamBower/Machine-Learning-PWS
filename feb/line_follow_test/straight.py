from gpiozero import Motor

class Leaphy():
	def __init__(self):
		self.motorL = Motor(27, 22)
		self.motorR = Motor(24, 23)

		self.LMax = 0.2
		self.RMax = 0.2

	def stop(self):
		self.motorL.stop()
		self.motorR.stop()

	def move(self, l_speed, r_speed):
		l_speed *= self.LMax
		r_speed *= self.RMax
		self.motorL.forward(l_speed)
		self.motorR.forward(r_speed)
"""
		l_speed -= self.LMax
		r_speed -= self.RMax
		print(f"{l_speed} | {r_speed}")
		if l_speed > 0:
			self.motorL.forward(l_speed)
		elif l_speed < 0:
			if l_speed < 1:
				l_speed = -1
			self.motorL.backward(abs(l_speed))
		if r_speed > 0:
			self.motorR.forward(r_speed)
		elif r_speed < 0:
			if r_speed < 1:
				r_speed = -1
			self.motorR.backward(abs(r_speed))
"""
leaphy = Leaphy()
leaphy.move(1, 1)
while True:
	print("Moving")
