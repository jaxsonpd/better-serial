## 
# @file com_rx.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-06-30
# @brief This file contains the functionality to receive communications from
# the serial port and print them to the terminal

import string
import sys
import serial
import threading
import utils


class ComRxThread(threading.Thread):
    """
    A thread to receive values from the serial port and print them to the
    terminal.
    """
    def __init__(self, serial_port: serial.Serial, display: bool = False):
        """
        Initialise the thread to receive value from the serial port and print
        it to the terminal

        ### Params:
        serial_port : serial.Serial
            The serial port to read from
        display : bool = False
            Weather to display non printable characters
        """
        super().__init__(group=None, name="com_rx_thread")
        
        printable_chars = string.printable
        self.printable_char_bytes = bytes(printable_chars, 'ascii')

        self.serial_port = serial_port
        self.display = display

        self._stopper = threading.Event()
        self._stopper.clear()
    
    def stop(self):
        """
        Stop the thread
        """
        self._stopper.set()

    def stopped(self):
        """
        Check if the thread has been stopped
        """
        return self._stopper.is_set()

    def run(self):
        """
        Run the com receive thread
        """
        while (not self.stopped()):
            try:
                com_rx = self.serial_port.read(1)
            except serial.SerialException:
                utils.close_com_threads()
                continue

            if (com_rx == b''): # if empty don't print
                continue

            if (self.display):
                if (com_rx in self.printable_char_bytes):
                    print(com_rx.decode(), end="")
                else:
                    print(com_rx, end="")
            else:
                print(com_rx.decode(), end="")

            sys.stdout.flush()
        
