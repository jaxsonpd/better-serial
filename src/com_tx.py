## 
# @file com_tx.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-06-30
# @brief The file contains the functionality to send over the serial port.

import string
import serial

from get_char import getchar

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


def com_tx_local_thread_entry(port: serial.Serial) -> None:
    """
    Local edit serial transmit thread entry. This thread takes user input
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


def com_tx_dumb_thread_entry(port: serial.Serial) -> None:
    """
    Dumb terminal serial transmit thread entry. This thread takes user input
    and then sends it to the device one char at a time.

    ### Params:
    port: serial.Serial
        The serial port to write to
    """

    while (True):
        char = getchar()
        port.write(char.encode())