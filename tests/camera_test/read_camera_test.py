from serial import Serial

ser = Serial("/dev/ttyUSB0", 38400)
fh = open("image.jpg", "wb")


class JPEGImage(object):
    START_MAGIC = bytes([255, 216])  # FF D8
    END_MAGIC = bytes([255, 217])  # FF D9

    def __init__(self, fh):
        self.last_byte = bytes([0])
        self.jpeg_bytes = bytes()
        self.is_finished = False

    def update(self, byte):
        print(self.last_byte, byte)
        if self.is_finished:
            print("DONE!~!!!")
            return

        if self.last_byte + byte == self.START_MAGIC:
            print("found magic")
            self.jpeg_bytes += self.START_MAGIC
            return

        if self.jpeg_bytes[:2] == self.START_MAGIC:
            self.jpeg_bytes += byte

        if self.jpeg_bytes[-2:] == self.END_MAGIC:
            print("found magic")
            self.fh.write(self.jpeg_bytes)
            self.fh.close()
            self.is_finished = True

        self.last_byte = byte


jpeg = JPEGImage(fh)


def process_byte(s_byte):
    byte = bytes([int(s_byte, 16)])
    jpeg.update(byte)


while True:
    line = ser.readline().decode("ascii").strip()

    if not line:
        continue

    print(line)

    for s_byte in line.split(" "):
        process_byte(s_byte)
