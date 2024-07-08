##
# @file main.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 27-06-2024
# @brief the main file for the better-terminal app containing the main loop 
# and helper Functions

import threading
import serial

from get_char import getchar
from cmd_args import setup_cmd_args
from com_rx import com_rx_thread_entry
from com_tx import com_tx_local_thread_entry, com_tx_dumb_thread_entry
from configuration import Config, ConfigDict

def load_settings() -> ConfigDict:
    """
    Load settings from a file if it exists otherwise create it from the default
    configuration.

    ### Returns:
    out : ConfigDict
        The loaded configuration object
    """
    config = ConfigDict()
    config = Config.load_json("settings.json")

    return config
        


def open_serial_port(port: str, baud: int, data: int, parity: str,
    stop: int, timeout: float) -> serial.Serial:
    """
    Continuously attempt to open a serial port.

    ### Param:
    port: string
        The serial port to open
    baud: int
        The baud rate to open the serial port
    data: int
        The number of data bits
    parity: str 
        The whether parity is enabled
    stop: int
        The number of stop bits
    timeout: float
        The time to wait before timing out on a serial read

    ### Returns:
     : serial.Serial
        The opened serial port
    """
    serial_started = False
    first_print = True
    while (not serial_started):
        try:
            port = serial.Serial(port=port, baudrate=baud, 
                bytesize=data, parity=parity, stopbits=stop,
                timeout=timeout)
            serial_started = True
            
        except serial.serialutil.SerialException:
            if (first_print):
                print("Serial port open error please review settings")

            first_print = False
        except:
            exit(0)

    print(f"Serial monitor started: {data}, {stop}, {baud}, {parity}")

    return port

def main() -> None:
    """
    The main function for the project 
    """
    # load settings file
    app_settings = load_settings()

    parser = setup_cmd_args()
    args = parser.parse_args()

    # Wait for serial port to open
    port = open_serial_port(args.port, args.baud, args.data, args.parity,
        args.stop, 0.5)

    # Setup application threads
    com_tx_thread = threading.Thread()

    if (args.mode == "local"):
        print(f"In local edit mode with display {args.display}.")
        com_tx_thread = threading.Thread(group=None, 
            target=com_tx_local_thread_entry, args=(port, ))
        
    elif (args.mode == "dumb"):
        print(f"In dumb mode with display {args.display}.")
        com_tx_thread = threading.Thread(group=None, 
            target=com_tx_dumb_thread_entry, args=(port, ))

    com_rx_thread = threading.Thread(group=None, target=com_rx_thread_entry,
        args=(port, args.display, ))
    
    # start threads
    com_tx_thread.start()
    com_rx_thread.start()

    com_tx_thread.join()
    com_rx_thread.join()

if __name__ == "__main__":
    main()
