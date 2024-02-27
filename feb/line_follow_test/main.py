import image_operations, line_find, motor_operations
import math, copy
from datetime import datetime, timedelta
from threading import Thread

line_split = 21
if (line_split % 2) == 0:
	line_split += 1
middle_line = math.floor(line_split / 2)

line_interval = timedelta(seconds=0.025)
motor_active = True

def locate_line(img):
	print(2)
	line_img = image_operations.line_image(img, line_split)
	print(3)
	line_vals, line_result = line_find.locate_line(line_img, line_split)
	print(line_vals)
	print(line_result)
	print()
	return line_vals, line_result

def line_follow(img):
	line_vals, line_result = locate_line(img)
	if line_result == middle_line:
		print("straight")
		motor_operations.leaphy.move(1, 1)
	elif line_result < middle_line:
		part = int(abs(int(middle_line) - int(line_result)))
		print(part, type(part))
		angle = (part**2)/100
		motor_operations.leaphy.move(angle, (line_result - middle_line))
	elif line_result > middle_line:
		part = int(abs(line_result - middle_line))
		print(part)
		angle = (part**2)/100
		motor_operations.leaphy.move(angle, (line_result - middle_line))

def image():
	image_operations.picture()
#	print("c")
	img = image_operations.load_image()
#	print("d")
	return img

def main():
	a = datetime.now()
	next_line_time = a + line_interval

	while 1:
		a = datetime.now()
		print(a)
		img = image()
#		print("b")
		if a >= next_line_time:
#			print(1)
			next_line_time = a + line_interval
			t1 = Thread(target=line_follow, args=(img,))
			t1.start()

if __name__ == "__main__":
	main()
