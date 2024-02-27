import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import io

# Function to generate frames with a changing graph
def make_frame(t):
    # Generate example data that changes over time
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x + t)
    y2 = np.cos(x+t)
    y3 = np.tan(x+t)

    # Create a new plot for each frame
    fig, ax = plt.subplots(2, 2, figsize=(1366/100, 768/100))
    #fig.delaxes(ax[0,0])
    img = mpimg.imread("C:/Users/willi/Downloads/a7f7c8532f5650a1c6869f581d5ec0f4.jpg")
    ax[0, 0].imshow(img)
    ax[0, 0].axis('off')
    ax[0, 1].plot(x, y, label="Motors")
    ax[1, 0].plot(x, y2, label="Model output")
    ax[1, 1].plot(x, y3, label="Line output")
    ax[0, 1].set_ylim(-1, 1)
    ax[1, 0].set_ylim(0, 1)
    ax[1, 1].set_ylim(0, 100)
    ax[0, 1].set_title("Motors")
    ax[1, 0].set_title("Model output")
    ax[1, 1].set_title("Line output")
    #fig.set_title('Changing Graph')
    plt.tight_layout()

    # Convert the plot to an image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = plt.imread(buf)

    plt.close(fig)

    return image

# Set up variables for changing time between frames (duration of frames)
time_between_frames = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]  # Varying time between frames in seconds

# Create a list of frames with varying time delays
frames = []
current_time = 0.0
for time_delay in time_between_frames:
    frame = make_frame(current_time)
    frames.append((frame, time_delay))
    current_time += time_delay

# Get the dimensions from the first frame
height, width, _ = frames[0][0].shape

# Create a video writer for MP4 using H.264 codec
fourcc = cv2.VideoWriter_fourcc(*'avc1')
video_writer = cv2.VideoWriter('output_video.mp4', fourcc, 24, (width, height))

# Write frames to the video file with varying time delays
for frame, time_delay in frames:
    frame = (frame * 255).astype(np.uint8)  # Convert to uint8 for OpenCV
    video_writer.write(frame)
    cv2.waitKey(int(time_delay * 1000))  # Convert time delay to milliseconds

# Release the video writer
video_writer.release()
cv2.destroyAllWindows()
