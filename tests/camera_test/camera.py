from serial import Serial
from time import sleep
import struct
from io import BytesIO


def x(byteStr):
    byteStr = str(byteStr)
    return ''.join(["%02X " % ord(x) for x in byteStr]).strip()

RESET = b"\x56\x00\x26\x00"
TAKE_PIC = b"\x56\x00\x36\x01\x00"
READ_SIZE = b"\x56\x00\x34\x01\x00"

ser = Serial("/dev/ttyUSB0", 115200)


def pr():
    while ser.inWaiting():
        b = ser.read()
        try:
            print(b.decode("ascii"), end="")
        except UnicodeDecodeError:
            print(b, end="")


def clean_ser(ser=ser):
    while ser.inWaiting():
        ser.read()


def reset(ser=ser, delay=4):
    clean_ser(ser)

    ser.write(RESET)
    sleep(delay)
    clean_ser(ser)

    return True


def take_picture(ser=ser):
    clean_ser(ser)

    ser.write(TAKE_PIC)
    sleep(0.01)
    clean_ser(ser)

    return True


def read_file_size(ser=ser):
    clean_ser(ser)

    ser.write(READ_SIZE)
    sleep(0.01)
    ser.read(7)  # fixed amount

    file_size_xh = ser.read(1)
    file_size_xl = ser.read(1)

    return (file_size_xh, file_size_xl)


def change_baud_rate(ser=ser):
    clean_ser(ser)

    sleep(0.025)

    ser.write(b"\x56\x00\x24\x03\x01")
    ser.write(b"\x0D\xA6")  # 115200

    sleep(0.025)
    ser.read(5)

    return True


def dump(io_obj, fn="asd.jpeg"):
    with open(fn, "wb") as f:
        f.write(io_obj.getvalue())


def take_pic():
    reset()
    take_picture()
    xh, xl = read_file_size()

    print(int.from_bytes(xh + xl, byteorder="big"))

    sleep(1)

    a = 0x00
    buff = BytesIO()

    done = False

    while not done:
        j = 0x00
        k = 0x00
        count = 0

        mh = a // 0x100
        ml = a % 0x100

        ser.write(b"\x56\x00\x32\x0C\x00\x0A\x00\x00")
        ser.write(bytes([mh, ml]))
        ser.write(b"\x00\x00")
        ser.write(b"\x00\x20")  # data to read (chunksize)
        ser.write(b"\x00\x0A")
        a += 0x20

        sleep(0.050)

        last_b = b"\x11"
        while ser.inWaiting():
            b = ser.read()
            k += 1
            if k > 5 and j < 32 and not done:
                buff.write(b)

                if last_b == b"\xFF" and b == b"\xD9":
                    done = True

                j += 1
                count += 1

            last_b = b

    return buff
