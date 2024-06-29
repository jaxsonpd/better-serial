## 
# @file local_line_mode.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-06-29
# @brief Local line editing terminal mode to allow special char to be sent

import serial
import threading
import sys
import string

# Possible escape characters
escape_chars = ['n', 'r', 't', 'b', 'f', 'o', 'x', '\\']

def convert_to_bytes(input_str: string) -> bytearray:
    """
    convert the provided string into a byte array without escaping \. This
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
        if (input_str[char_num] == '\\' 
            and char_num < (len(input_str) - 1)): # escape sequence
            
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


def com_tx_thread_entry(port: serial.Serial) -> None:
    """
    Send to device serial transmit thread entry. This thread takes user input
    and then sends it to the device including non printable chars entered in
    the normal python format (e.g. \x00).

    ### Params:
    port: serial.Serial
        The serial port to write to
    """

    while (True):
        str_to_send = input()

        output_bytes = convert_to_bytes(str_to_send)
        output_bytes.append(13)

        port.write(output_bytes) 


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

def local_line_mode(port: serial.Serial , display: bool = False) -> None:
    """
    Local line editing mode (and thus special char sending mode) application

    port: serial.Serial
        The serial port to write to
    
    display : bool = False
        Whether to print non displayable characters that are read from the 
        serial port
    """
    print(f"In local edit mode with display {display}.")

    # Setup threads
    com_tx_thread = threading.Thread(group=None, target=com_tx_thread_entry,
        args=(port, ))
    
    com_rx_thread = threading.Thread(group=None, target=com_rx_thread_entry,
        args=(port, display))

    # Run threads    
    com_tx_thread.start()
    com_rx_thread.start()

    com_tx_thread.join()
    com_rx_thread.join()