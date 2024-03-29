#!/usr/bin/env python

# Very simple serial terminal
# (C)2002-2011 Chris Liechti <cliechti@gmx.net>

# Input characters are sent directly (only LF -> CR/LF/CRLF translation is
# done), received characters are displayed as is (or escaped trough pythons
# repr, useful for debug purposes)

"""
Sets up an interactable terminal to the radio-module via a serial interface.
Also saves received lines to a log file and
communicates via a communication file with the feeder.
"""

import sys
import os

import serial
import threading

import termios

from groundstation.config import COM_FILE
from groundstation.utilities import discover_serial_port, listener_get_log_file


# LOG
LOG_FILE = listener_get_log_file()
log_handle = open(LOG_FILE, "w")

# Communication file
os.remove(COM_FILE)
os.mkfifo(COM_FILE)
com_handle = open(COM_FILE, "w")


EXITCHARCTER = chr(0x1d)

PORT = discover_serial_port()
BAUDRATE = 9600

RTS = None
DTR = None

XONXOFF = False
RTSCTS = False

ECHO = False

PARITY = "N"


def character(b):
    """
    Returns the decoded character ``b``.
    """
    return b.decode('latin1')

CRLF = serial.to_bytes([13, 10])

X00 = serial.to_bytes([0])
X0E = serial.to_bytes([0x0e])


class Console(object):
    """
    The ``Console`` class is an abstraction upon the console interface.
    Handles setting up and tearing down the console interface.
    """
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old = None

    def setup(self):
        """
        Sets up the console interface.
        """
        self.old = termios.tcgetattr(self.fd)
        new = termios.tcgetattr(self.fd)
        new[3] = new[3] & ~termios.ICANON & ~termios.ECHO & ~termios.ISIG
        new[6][termios.VMIN] = 1
        new[6][termios.VTIME] = 0
        termios.tcsetattr(self.fd, termios.TCSANOW, new)

    def getkey(self):
        """
        Read a single character from the console.
        """
        c = os.read(self.fd, 1)
        return c

    def cleanup(self):
        """
        Clean up the console.
        """
        if self.old is not None:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old)

console = Console()

sys.exitfunc = console.cleanup  # terminal modes have to be restored on exit...


class Miniterm(object):
    """
    The ``Miniterm`` class defines the structure of the terminal interface,
    in charge of sending and receiving data.
    """
    def __init__(self, port, baudrate, parity, rtscts, xonxoff, echo=False):
        self.serial = serial.serial_for_url(port, baudrate, parity=parity,
                                            rtscts=rtscts, xonxoff=xonxoff,
                                            timeout=1)

        self.echo = echo
        self.newline = CRLF
        self.dtr_state = True
        self.rts_state = True
        self.break_state = False

    def _start_reader(self):
        """
        Start reader thread.
        """
        self._reader_alive = True
        # start serial->console thread
        self.receiver_thread = threading.Thread(target=self.reader)
        self.receiver_thread.setDaemon(True)
        self.receiver_thread.start()

    def _stop_reader(self):
        """
        Stop reader thread only, wait for clean exit of thread.
        """
        self._reader_alive = False
        self.receiver_thread.join()

    def start(self):
        """
        Starts the terminal.
        """
        self.alive = True
        self._start_reader()
        # enter console->serial loop
        self.transmitter_thread = threading.Thread(target=self.writer)
        self.transmitter_thread.setDaemon(True)
        self.transmitter_thread.start()

    def stop(self):
        """
        Stops the terminal.
        """
        self.alive = False

    def join(self, transmit_only=False):
        """
        Joins the terminal, blocking with the subthreads of the terminal.
        """
        self.transmitter_thread.join()
        if not transmit_only:
            self.receiver_thread.join()

    def reader(self):
        """
        Loop and copy serial->console.
        """
        try:
            while self.alive and self._reader_alive:
                data = character(self.serial.read(1))

                log_handle.write(data)
                com_handle.write(data)

                # direct output, just have to care about newline setting
                sys.stdout.write(data)

                sys.stdout.flush()
                log_handle.flush()
                com_handle.flush()
        except serial.SerialException:
            self.alive = False
            # would be nice if the console reader could be interruptted at this
            # point...
            log_handle.close()
            com_handle.close()
            raise

    def writer(self):
        """
        Loop and copy console->serial until EXITCHARCTER character is
        found. When MENUCHARACTER is found, interpret the next key
        locally.
        """
        try:
            while self.alive:
                try:
                    b = console.getkey()
                except KeyboardInterrupt:
                    b = serial.to_bytes([3])
                c = character(b)

                if c == EXITCHARCTER:
                    self.stop()
                    break  # exit app
                elif c == '\n':
                    self.serial.write(self.newline)  # send newline characters
                    if self.echo:
                        # local echo is a real newline in any case
                        sys.stdout.write(c)
                        sys.stdout.flush()
                else:
                    self.serial.write(b)  # send byte
                    if self.echo:
                        sys.stdout.write(c)
                        sys.stdout.flush()
        except:
            self.alive = False
            raise


def main():
    """
    Sets up a terminal and runs it.
    """
    try:
        miniterm = Miniterm(PORT, BAUDRATE, PARITY, rtscts=RTSCTS,
                            xonxoff=XONXOFF, echo=ECHO)
    except serial.SerialException as e:
        sys.stderr.write("could not open port %r: %s\n" % (PORT, e))
        sys.exit(1)

    miniterm.serial.setDTR(DTR)
    miniterm.dtr_state = DTR
    miniterm.serial.setRTS(RTS)
    miniterm.rts_state = RTS

    console.setup()
    miniterm.start()
    try:
        miniterm.join(True)
    except KeyboardInterrupt:
        pass

    sys.stderr.write("\n--- exit ---\n")
    miniterm.join()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    main()
