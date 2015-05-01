"""
Contains a tornado-based WebSocket server in charge of supplying
connected clients with live or replay data.
"""


import tornado.ioloop
import tornado.web
import tornado.websocket

from collections import deque

from pprint import pprint

import json

from .config import COM_FILE
from .parse import validate_line, parse_line
from .exceptions import MalformedPacket
from .calculate import (calculate_temp_NTC, calculate_press, calculate_height,
                        calculate_gyr)

PORT = 8081

GETTER_FREQUENCY = 10  # MS
POSTER_FREQUENCY = 100  # MS

com_handle = open(COM_FILE, "r")

clients = []

CACHE_SIZE = 100  # How many data points to keep in cache.
cache = deque(maxlen=CACHE_SIZE)


class DataWebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True  # All clients are welcome

    def open(self):
        clients.append(self)
        print("A client has opened a connection.")

        for data_point in cache:
            self.write_message(data_point)

    def on_close(self):
        clients.remove(self)
        print("A client closed its connection.")

    def on_message(self, message):
        print("[WARNNING] Got message: {}".format(message))


def broadcast(message):
    for client in clients:
        client.write_message(message)


line_buf = ""


def get_data():
    line = com_handle.readline()

    if "\n" not in line:
        line_buf += line
        return
    else:
        line = line_buf + line
        global line_buf
        line_buf = ""

    try:
        validate_line(line)
    except MalformedPacket:
        line = line.replace("\n", "")
        print("[WARNING] Got malformed packet: {}".format(line))
        return

    data = handle_line(line)

    post_data(data)

    print(line, end="")


def handle_line(line):
    data = parse_line(line)

    NTC = calculate_temp_NTC(data["NTC"])
    pressure = calculate_press(data["Press"])
    height = calculate_height(pressure)
    rpm = calculate_gyr(data["GyrZ"]) / 360 * 60

    graph_data = {
        "Time": data["Time"],
        "NTC": NTC,
        "Pressure": pressure,
        "Height": height,
        "Gyroscope": rpm
    }

    pprint(data)

    return graph_data


def post_data(data):
    json_data = json.dumps(data)

    broadcast(json_data)


app = tornado.web.Application([(r"/ws", DataWebSocket)])


if __name__ == '__main__':
    app.listen(PORT, "0.0.0.0")
    loop = tornado.ioloop.IOLoop.instance()

    getter = tornado.ioloop.PeriodicCallback(get_data, GETTER_FREQUENCY,
                                             io_loop=loop)
    getter.start()
    loop.start()
