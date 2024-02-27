import random, math, os
from PIL import Image, ImageDraw

def bezier_curve(p0, p1, p2, p3, n_points=100):
    points = []
    for t in range(n_points):
        t /= n_points - 1
        x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    return points

def add_noise(point, magnitude):
  x = point[0] + random.uniform(-magnitude, magnitude)
  y = point[1] + random.uniform(-magnitude, magnitude)
  return (x, y)

def add_jitter(point, magnitude):
    x = point[0] + random.uniform(-magnitude, magnitude)
    y = point[1] + random.uniform(-magnitude, magnitude)
    return (x, y)

def generate_image():
  width = 960
  height = 1080
  image = Image.new("RGB", (width, height), "black")
  draw = ImageDraw.Draw(image)

  circle_radius = random.randint(20, min(width, height) // 4)
  circle_x = random.randint(circle_radius, width - circle_radius)
  circle_y = random.randint(circle_radius, height - circle_radius)

  draw.ellipse((circle_x - circle_radius, circle_y - circle_radius, circle_x + circle_radius, circle_y + circle_radius), fill="white")
  center_radius = int((circle_radius // 4) * 3)
  draw.ellipse((circle_x - center_radius, circle_y - center_radius, circle_x + center_radius, circle_y + center_radius), fill="black")

  num_patches = random.randint(3, 6)
  patch_size = circle_radius // 2
  for _ in range(num_patches):
      patch_x = random.randint(circle_x - circle_radius, circle_x + circle_radius)
      patch_y = random.randint(circle_y - circle_radius, circle_y + circle_radius)
      for x in range(patch_x - patch_size, patch_x + patch_size):
          for y in range(patch_y - patch_size, patch_y + patch_size):
              if (x - circle_x) ** 2 + (y - circle_y) ** 2 <= circle_radius ** 2:
                  if random.random() < 0.5:  # Adjust this probability for noise density
                      draw.point((x, y), fill="black")

  num_parts = random.randint(40, 60)  # Adjust the range of parts as needed
  for i in range(num_parts):
    angle_start = random.uniform(i*((2*math.pi)/num_parts), i*((2*math.pi)/num_parts))
    angle_end = angle_start + random.uniform(math.pi/6, math.pi/3)
#    angle_start = random.uniform(0, 2*math.pi)
#    angle_end = angle_start + random.uniform(math.pi/6, math.pi/3)  # Adjust the range of angles as needed
    dist_from_center = random.uniform(0.85*circle_radius, 1*circle_radius)
    angle_mid = (angle_start + angle_end) / 2
    
    x_start = circle_x + dist_from_center * math.cos(angle_start)
    y_start = circle_y + dist_from_center * math.sin(angle_start)
    
    x_mid = circle_x + circle_radius * math.cos(angle_mid)
    y_mid = circle_y + circle_radius * math.sin(angle_mid)
    
    x_end = circle_x + dist_from_center * math.cos(angle_end)
    y_end = circle_y + dist_from_center * math.sin(angle_end)
    
    num_control_points = random.randint(4, 4)  # Random number of control points for jaggedness
    control_points = [add_jitter((x_start, y_start), 5)]
    for _ in range(num_control_points - 2):
      control_points.append(add_jitter((random.uniform(x_start, x_end), random.uniform(y_start, y_end)), 5))
    control_points.append(add_jitter((x_end, y_end), 5))
    
    bezier_points = bezier_curve(*control_points)
    draw.polygon(bezier_points, fill="black")

  image = image.resize((width//10, height//10))
  
  return image, ((circle_y - circle_radius), (circle_x - circle_radius), (circle_y + circle_radius), circle_x + circle_radius)

os.mkdir("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/detector/model_data")
if __name__ == "__main__":
  labels = {}
  for i in range(10):
    img, coordinates = generate_image()
    name = ("0"*(4-len(str(i))))+ (f"{i}")
    img.save(f"C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/detector/model_data/circle{name}.jpg")
    labels[i] = (coordinates)
    print(i)
  import json
  with open("labels.json", "w") as f:
    f.write(json.dumps(labels, indent=4))