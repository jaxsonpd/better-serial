##
# @file main.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 27-06-2024
# @brief the main file for the better-terminal app containing the main loop 
# and helper Functions

from get_char import getchar
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
    port = serial.Serial("/dev/ttyUSB0", 57600, timeout=0.5)

    keyboard.add_hotkey('ctrl + shift + z', callback=com_tx, args={port})
    keyboard.add_hotkey('ctrl + c', callback=exit)


    while (True):
        if (not com_tx_flag):
            com_rx(port)

        
    


if __name__ == "__main__":
    main()
