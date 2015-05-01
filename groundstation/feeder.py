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

from .config import GENERAL, FEEDER, BIND_ADDRESS
from .parse import validate_line, parse_line
from .exceptions import MalformedPacket
from .calculate import (calculate_temp_NTC, calculate_press, calculate_height,
                        calculate_gyr)

com_handle = open(GENERAL["com_file"], "r")

clients = []

cache = deque(maxlen=FEEDER["cache_size"])


class BaseWebSocket(tornado.websocket.WebSocketHandler):
    """
    A base class for all WebSocket interfaces.
    """
    def check_origin(self, origin):
        return True  # All clients are welcome


class LiveDataWebSocket(BaseWebSocket):
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


app = tornado.web.Application([(r"/live", LiveDataWebSocket)])


if __name__ == '__main__':
    app.listen(FEEDER["port"], BIND_ADDRESS)
    loop = tornado.ioloop.IOLoop.instance()

    getter = tornado.ioloop.PeriodicCallback(get_data, FEEDER["frequency"],
                                             io_loop=loop)
    getter.start()
    loop.start()
