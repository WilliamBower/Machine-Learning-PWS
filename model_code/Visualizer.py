import matplotlib.pyplot as plt
EPOCHS = 2
epochs_range = range(EPOCHS)
acc = [0.4833333194255829, 0.5383333563804626]
loss = [1442.93896484375, 122.79529571533203]

plt.plot(acc)
plt.plot(loss)
plt.xlabel("EPOCHS")
plt.legend(["acc", "loss"], loc="upper left")
plt.show()