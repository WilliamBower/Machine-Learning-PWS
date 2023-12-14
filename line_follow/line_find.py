import numpy as np

threshold = 50

def locate_line(img, parts):
    height, width = img.shape[0], img.shape[1]
    results = []
    for i in range(parts):
        #select part of image
        step1 = img.copy()[0:height, (int(width/parts*i)):(int(width/parts*(i+1)))]

        #count pixels below threshold
        step2 = np.sum(step1 <= threshold)
        results.append(step2)
    
    #find part with most line pixels and return part
    result = results.index(max(results))
    return result