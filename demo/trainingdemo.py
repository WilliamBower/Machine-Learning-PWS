import numpy as np
import matplotlib.pyplot as plt
import cv2
import io
import csv

accuracy = []
loss = []
val_acc = []
val_loss = []
val_x = []

def make_frame():
    x = np.linspace(0, (len(accuracy)-1), (len(accuracy)), dtype='int')
    y1 = accuracy
    y2 = loss
    x2 = val_x
    y3 = val_acc
    y4 = val_loss

    fig, ax = plt.subplots(2, 1, figsize=(1366/100, 768/100))
    ax[0].plot(x, y1, label="Train")
    ax[0].plot(x2, y3, label="Val")
    ax[0].set_title("Accuracy")
    ax[0].legend()
    ax[1].plot(x, y2, label="Train")
    ax[1].plot(x2, y4, label="Val")
    ax[1].set_title("Loss")
    ax[1].legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image = plt.imread(buf)
    plt.close(fig)
    return image

batch_data = []
with open("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/demo/batches.csv", "r") as f:
    batch_reader = csv.reader(f)
    for row in batch_reader:
        batch_data.append(row)
batch_data.pop(0)
accuracy.append(float(batch_data[0][1]))
loss.append(float(batch_data[0][2]))
batch_data.pop(0)

valid_data = []
with open("C:/Users/willi/Documents/GitHub/Machine-Learning-PWS/demo/valid.csv", "r") as f:
    valid_reader = csv.reader(f)
    for row in valid_reader:
        valid_data.append(row)
valid_data.pop(0)

frames = []
for value in batch_data:
    print(value)
    accuracy.append(float(value[1]))
    loss.append(float(value[2]))
    if int(valid_data[0][1]) == len(accuracy):
        print(valid_data[0])
        val_acc.append(float(valid_data[0][2]))
        val_loss.append(float(valid_data[0][3]))
        val_x.append(len(accuracy))
        valid_data.pop(0)
    frames.append(make_frame())

height, width, _ = frames[0].shape

fourcc = cv2.VideoWriter_fourcc(*'avc1')
video_writer = cv2.VideoWriter('train_video.mp4', fourcc, 24, (width, height))

for frame in frames:
    frame = (frame * 255).astype(np.uint8)
    for _ in range(int(60 * 0.1)):
        video_writer.write(frame)
    #cv2.waitKey(int(0.8 * 1000))

video_writer.release()
cv2.destroyAllWindows()