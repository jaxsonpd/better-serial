## 
# @file com_rx.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-06-30
# @brief This file contains the functionality to receive communications from
# the serial port and print them to the terminal

import string
import sys
import serial

def com_rx_thread_entry(port: serial.Serial, display: bool = False) -> None:
    """
    Receive from device thread entry. This thread reads from the serial port and
    prints one byte at a time to the terminal.

    ### Params:
    port : serial.Serial
        The serial port to print to

    display : bool = False
        Whether to print non displayable characters that are read from the 
        serial port
    """
    printable_chars = string.printable
    # printable_chars = printable_chars.replace('~', '') # Test its working

    printable_char_bytes = bytes(printable_chars, 'ascii')

    while (True):
        com_rx = port.read(1)

        if (com_rx == b''): # if empty don't print
            continue

        if (display):
            if (com_rx in printable_char_bytes):
                print(com_rx.decode(), end="")
            else:
                print(com_rx, end="")
        else:
            print(com_rx.decode(), end="")

        sys.stdout.flush()