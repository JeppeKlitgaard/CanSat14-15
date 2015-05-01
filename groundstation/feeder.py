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
from .parse import easy_parse_line
from .exceptions import InvalidLine
from .utilities import Buffer

com_handle = open(GENERAL["com_file"], "r")
line_buffer = Buffer(com_handle)

clients = []

cache = deque(maxlen=FEEDER["cache_size"])


class BaseWebSocket(tornado.websocket.WebSocketHandler):
    """
    A base class for all WebSocket interfaces.
    """
    def check_origin(self, origin):
        return True  # All clients are welcome


class LiveDataWebSocket(BaseWebSocket):
    """
    Serves clients connected to the live endpoint with live data.
    """
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


class ReplayWebSocket(BaseWebSocket):
    """
    Serves clients connected to the replay endpoint.
    """


def broadcast(message):
    for client in clients:
        client.write_message(message)


def get_data():
    line = line_buffer.get_line()

    if not line:
        return

    try:
        data = easy_parse_line(line)
    except InvalidLine:
        return

    pprint(data)

    post_data(data)

    print(line, end="")


def post_data(data):
    json_data = json.dumps(data)

    broadcast(json_data)


app = tornado.web.Application([
    (r"/live", LiveDataWebSocket)
    (r"/replay", ReplayWebSocket)
])


if __name__ == '__main__':
    app.listen(FEEDER["port"], BIND_ADDRESS)
    loop = tornado.ioloop.IOLoop.instance()

    getter = tornado.ioloop.PeriodicCallback(get_data, FEEDER["frequency"],
                                             io_loop=loop)
    getter.start()
    loop.start()
