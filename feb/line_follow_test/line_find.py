import numpy as np

threshold = 50

def locate_line(img, parts):
	height, width = img.shape[0], img.shape[1]
	results = []
	for i in range(parts):
		part = img.copy()[0:height, (int(width/parts*i)):(int(width/parts*(i+1)))]
		results.append(np.sum(part <= threshold))

	lowest_index = 0
	highest_index = 0
	highest_val = -5
	for index, value in enumerate(results):
		if value > highest_val:
			highest_val, lowest_index, highest_index = value, index, index
		elif value == highest_val:
			highest_index = index
	line_loc = (lowest_index + highest_index)/2
	return results, line_loc
