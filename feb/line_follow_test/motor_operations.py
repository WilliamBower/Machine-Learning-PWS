from gpiozero import Motor

scaling = 0.1
scaling2 = 0.4
class Leaphy():
	def __init__(self):
		self.motorL = Motor(27, 22)
		self.motorR = Motor(24, 23)

		self.LMax = 0.2
		self.RMax = 0.2

	def stop(self):
		self.motorL.stop()
		self.motorR.stop()

	def move(self, angle, part):
		if part > 1:
			print(angle*scaling2)
			l_speed = self.LMax + (angle * scaling)
			r_speed = self.RMax - (angle * scaling2)
		elif part < 1:
			print(angle * scaling2)
			l_speed = self.LMax - (angle * scaling2)
			r_speed = self.RMax + (angle * scaling)
		else:
			l_speed = self.LMax
			r_speed = self.RMax
		print(l_speed)
		print(r_speed)
		if l_speed < -1 or l_speed > 1:
			l_speed /= l_speed
		if r_speed < -1 or r_speed > 1:
			r_speed /= r_speed
		if l_speed < 0:
			self.motorL.backward(abs(l_speed))
		else:
			self.motorL.forward(l_speed)
		if r_speed < 0:
			self.motorR.backward(abs(r_speed))
		else:
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
