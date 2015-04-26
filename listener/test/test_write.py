import time

f = open("test.log", "w")

i = 0
while True:
    i += 1

    msg = "Beer count: {}\n".format(str(i))
    f.write(msg)
    f.flush()
    print(msg, end="")

    time.sleep(0.25)
