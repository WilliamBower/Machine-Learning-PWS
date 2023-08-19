from threading import Thread
import time

def main1():
    for i in range(3):
        print(1)
        time.sleep(5)
        print(2)

def main2():
    for i in range(5):
        print(3)
        time.sleep(3)
        print(4)

t1 = Thread(target=main1)
t2 = Thread(target=main2)
if __name__ == "__main__":
    t1.start()
    t2.start()
    #in plaats van main()