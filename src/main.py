##
# @file main.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 27-06-2024
# @brief the main file for the better-terminal app containing the main loop 
# and helper Functions

import serial.serialutil
from get_char import getchar
from cmd_args import setup_cmd_args
from local_line_mode import local_line_mode

import serial


def main() -> None:
    """
    The main function for the project 
    """
    parser = setup_cmd_args()
    args = parser.parse_args()

    serial_started = False
    first_print = True
    while (not serial_started):
        try:
            port = serial.Serial(port=args.port, baudrate=args.baud, 
                bytesize=args.data, parity=args.parity, stopbits=args.stop,
                timeout=0.5)
            serial_started = True
            
        except serial.serialutil.SerialException:
            if (first_print):
                print("Serial port open error please review settings")

            first_print = False
        except:
            exit(0)
    
    print(f"Serial monitor started: {args.data}, {args.stop}, {args.baud},",
        f"{args.parity}")

    if (args.mode == "local"):
        local_line_mode(port, args.display)
    elif (args.mode == "dumb"):
        print("Started Dumb")

if __name__ == "__main__":
    main()
