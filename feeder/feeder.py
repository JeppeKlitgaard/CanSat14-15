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

from .config import CACHE_SIZE, PORT, FREQUENCY

from groundstation.config import COM_FILE, BIND_ADDRESS
from groundstation.parse import easy_parse_line
from groundstation.exceptions import InvalidLine
from groundstation.utilities import Buffer

com_handle = open(COM_FILE, "r")
line_buffer = Buffer(com_handle)

clients = []

cache = deque(maxlen=CACHE_SIZE)


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
        """
        Called when a client opens the connection.
        """
        clients.append(self)
        print("A client has opened a connection.")

        for data_point in cache:
            self.write_message(data_point)

    def on_close(self):
        """
        Called when a client closes the connection.
        """
        clients.remove(self)
        print("A client closed its connection.")

    def on_message(self, message):
        """
        Called when a client sends a message.
        """
        print("[WARNNING] Got message: {}".format(message))


class ReplayWebSocket(BaseWebSocket):
    """
    Serves clients connected to the replay endpoint.
    """


def broadcast(message):
    """
    Broadcasts a message to all the connected clients.
    """
    for client in clients:
        client.write_message(message)


def get_data():
    """
    Called by the ioloop to get data from the listener.
    """
    line = line_buffer.get_line()

    if not line:
        return

    try:
        data = easy_parse_line(line)
    except InvalidLine:
        return

    pprint(data)

    rel_data = {
        "Time": data["Time"],
        "Temp": data["BMP180_Temp"],
        "Pressure": data["Pressure"],
        "Height": data["Height"],
        "Gyroscope": data["Gyroscope"],
        "Latitude": data["Latitude"],
        "Longitude": data["Longitude"]
    }

    post_data(rel_data)

    print(line, end="")


def post_data(data):
    """
    Called by ``get_data``.

    Sends ``data`` to the connected clients.
    """
    json_data = json.dumps(data)

    broadcast(json_data)


app = tornado.web.Application([
    (r"/live", LiveDataWebSocket),
    (r"/replay", ReplayWebSocket)
])


if __name__ == '__main__':
    app.listen(PORT, BIND_ADDRESS)
    loop = tornado.ioloop.IOLoop.instance()

    getter = tornado.ioloop.PeriodicCallback(get_data, FREQUENCY,
                                             io_loop=loop)
    getter.start()
    loop.start()
