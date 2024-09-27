##
# @file main.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 27-06-2024
# @brief the main file for the better-terminal app containing the main loop 
# and helper Functions

import serial
import datetime


from cmd_args import setup_cmd_args
from com_rx import ComRxThread
from com_tx import ComTxThread
import utils


from configuration import Config, ConfigDict

def load_settings() -> tuple[ConfigDict, ConfigDict]:
    """
    Load settings from a file if it exists otherwise create it from the default
    configuration.

    ### Returns:
    out : ConfigDict
        The default configuration 
    out : ConfigDict
        THe config dictionary for the current configuration
    """
    default_cfg = ConfigDict()

    current_cfg = ConfigDict()
    current_cfg.version = 1

    default_cfg = Config.load_json("default-settings.json")
    
    return default_cfg, current_cfg

def transpose_args(args, current_cfg: ConfigDict) -> None:
    """
    Copy the parser args to the current configuration

    ### Params:
    args : 
        The parser arguments
    current_cfg
        The current configurations
    """
    current_cfg.mode = args.mode
    current_cfg.serial = ConfigDict()
    current_cfg.serial.port = args.port
    current_cfg.serial.baud = args.baud
    current_cfg.serial.data = args.data
    current_cfg.serial.parity = args.parity
    current_cfg.serial.stop = args.stop
    
    current_cfg.terminal = ConfigDict()
    current_cfg.terminal.display_npc = args.display
    current_cfg.terminal.new_line_char = "NaN"

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
                print(f"{utils.get_time_str()} Serial port waiting to open" \
                      "(Check settings if connected) \r")

            first_print = False
        except:
            exit(0)

    print(f"{utils.get_time_str()} Serial monitor started: {data}, {stop}, {baud}, {parity}")

    return port

def main() -> None:
    """
    The main function for the project 
    """
    # load settings file
    default_cfg, current_cfg = load_settings()

    parser = setup_cmd_args(default_cfg)
    args = parser.parse_args()

    transpose_args(args, current_cfg)

    while (True):
        # Wait for serial port to open
        port = open_serial_port(current_cfg.serial.port, current_cfg.serial.baud, 
            current_cfg.serial.data, current_cfg.serial.parity, 
            current_cfg.serial.stop, 0.5)

        print(f"{utils.get_time_str()} In {current_cfg.mode} mode with display " \
            f"{current_cfg.terminal.display_npc}.")

        com_tx_thread = ComTxThread(port, current_cfg.mode)
        
        com_rx_thread = ComRxThread(port, current_cfg.terminal.display_npc)

        # start threads
        com_tx_thread.start()
        com_rx_thread.start()

        com_rx_thread.join()
        print(f"\r\n{utils.get_time_str()} Lost connection\r")
        com_tx_thread.join()
        


        port.close()

if __name__ == "__main__":
    main()
