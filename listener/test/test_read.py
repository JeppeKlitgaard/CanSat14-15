import time

f = open("test.log", "r")

while True:
    print(f.readline(), end="")

    time.sleep(0.1)
