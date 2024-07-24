## 
# @file com_tx.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-06-30
# @brief The file contains the functionality to send over the serial port.

import string
import serial
import os
import sys
import threading
import utils

from get_char import getchar

# Possible escape characters
escape_chars = ['n', 'r', 't', 'b', 'f', 'o', 'x', '\\']

def convert_to_bytes(input_str: string) -> bytearray:
    """
    convert the provided string into a byte array without escaping \\. This
    allows the sending of non printable chars to the device. 

    ### Params:
    input_str : string
        the input string to convert

    ### Return:
     : bytearray
        The converted string
    """
    def print_error():
        print("error: bad escape sequence line not sent")
        return bytearray(b'')

    output_bytes = bytearray(b'')

    char_num = 0

    while (char_num < len(input_str)):
        # escape sequences
        if (input_str[char_num] == '\\' 
            and char_num < (len(input_str) - 1)): 
            
            if (input_str[char_num+1] == 'n'):
                    output_bytes.append(10)
            elif (input_str[char_num+1] == 'r'):
                    output_bytes.append(13)
            elif (input_str[char_num+1] == 't'):
                    output_bytes.append(9)
            elif (input_str[char_num+1] == 'b'):
                    output_bytes.append(8)
            elif (input_str[char_num+1] == 'f'):
                    output_bytes.append(12)
            elif (input_str[char_num+1] == '\\'):
                    output_bytes.append(92)
            elif (input_str[char_num+1] =='x'
                  and char_num < len(input_str) - 3):
                    output_bytes.append(int(input_str[char_num+2:char_num+4], 
                        16))
                    char_num += 2
            elif (input_str[char_num+1] == 'o' 
                and char_num < len(input_str) - 4):
                    output_bytes.append(int(input_str[char_num+2:char_num+5], 
                        8))
                    char_num += 3
            else:
                    print_error()
                
            char_num += 1

        elif (input_str[char_num] == '\\'
            and not char_num < (len(input_str) - 1)):
            print_error()
        else:
            output_bytes.append(int.from_bytes(
                input_str[char_num].encode(), "big"))
        
        char_num += 1

    return output_bytes


class ComTxThread(threading.Thread):
    """
    A thread to send values to the serial port from the terminal.
    """
    def __init__(self, serial_port: serial.Serial, mode: str = "local"):
        """
        Initialise the thread to send values to the terminal from the 
        terminal.

        ### Params:
        serial_port : serial.Serial
            The serial port to send to
        mode : str = "local"
            The mode to use for the terminal (dumb or local)
        """
        super().__init__(group=None, name="com_tx_thread")

        self.serial_port = serial_port
        self.mode = mode

        self._stopper = threading.Event()
        self._stopper.clear()
    
    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()

    def run(self):
        """
        Run the sending thread
        """
        if (self.mode == "dumb"):
            self.run_dumb()
        elif (self.mode == "local"):
            self.run_local()

    def run_dumb(self):
        """
        Dumb terminal serial transmit thread entry. This thread takes user input
        and then sends it to the device one char at a time.
        """
        while (not self.stopped()):
            char = getchar()

            if (char == -1):
                continue
            elif (char == '\b'):
                print('\b\x20\b', end="")
                sys.stdout.flush()
            elif (char == '\x03'):
                os._exit(0)

            try: # Cannot use .is_open() as it is to slow
                self.serial_port.write(char.encode())
            except serial.SerialException:
                utils.close_com_threads()
                continue
            

    def run_local(self):
        """
        Local edit serial transmit thread entry. This thread takes user input
        and then sends it to the device including non printable chars entered in
        the normal python format (e.g. \x00).
        """
        try:
            while (not self.stopped()):
                str_to_send = input()

                output_bytes = convert_to_bytes(str_to_send)
                output_bytes.append(13) # \n

                try: # Cannot use .is_open() as it is to slow
                    self.serial_port.write(output_bytes)
                except serial.SerialException:
                    utils.close_com_threads()

        except EOFError:
            os._exit(0)

