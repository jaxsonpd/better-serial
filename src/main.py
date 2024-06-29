##
# @file main.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 27-06-2024
# @brief the main file for the better-terminal app containing the main loop 
# and helper Functions

from get_char import getchar
from cmd_args import setup_cmd_args
from local_line_mode import local_line_mode

import time
import keyboard 
import sys

import argparse
import serial

com_tx_flag = False

def com_tx(port: serial.Serial) -> None:
    """ 
    Callback from hotkey to trigger capture and sending of a string.

    ### Params:
    port : serial.Serial
        The serial port to read
    """
    global com_tx_flag 
    com_tx_flag = True

    str_to_send = input("tx >")
    str_to_send += "\r\n"
    print(str_to_send, end="")
    port.write(str_to_send.encode()) 

    com_tx_flag = False

def com_rx(port: serial.Serial) -> None:
    """
    Receive data from the com port and print it to the terminal.

    ### Params:
    port : serial.Serial
        The serial port to print to
    """
    com_rx = port.read(1)
    print(com_rx.decode(), end="")
    sys.stdout.flush()
    


def main() -> None:
    """
    The main function for the project 
    """
    # keyboard.add_hotkey('ctrl + shift + z', callback=com_tx, args={port})
    # keyboard.add_hotkey('ctrl + c', callback=exit)

    parser = setup_cmd_args()
    args = parser.parse_args()
    print(f"Serial monitor started: {args.data}, {args.stop}, {args.baud},",
        f"{args.parity}")

    port = serial.Serial(port=args.port, baudrate=args.baud, 
        bytesize=args.data, parity=args.parity, stopbits=args.stop,
        timeout=0.5)

    if (args.mode == "local"):
        local_line_mode(port, args.display)
    elif (args.mode == "dumb"):
        pass

if __name__ == "__main__":
    main()
