from serial import Serial


ser = Serial("/dev/ttyACM0", 9600)

while True:
    print(ser.read())
