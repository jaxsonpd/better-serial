## 
# @file cmd_args.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-06-29
# @brief Provides functionality to parse the command line arguments

import argparse

from configuration import ConfigDict

def setup_cmd_args(config: ConfigDict) -> argparse.ArgumentParser:
    """
    Setup the command line arguments that can be provided to the program
    
    ### Params:
    config : ConfigDict
        The configuration dictionary that contains the application settings

    ### Returns:
    out : argparse.ArgumentParser
        The argument parser configured for the application
    """
    parser = argparse.ArgumentParser(
        description="A simple serial monitoring application.")
    
    # Serial port settings
    serial_settings = parser.add_argument_group("Port Settings",
        "Serial port settings")
    
    serial_settings.add_argument("port", nargs="?", type=str, action="store",
        default=config.init_serial.port, 
        help=f"port to open (D: {config.init_serial.port})")
    
    serial_settings.add_argument("baud", nargs="?", type=int, action="store",
        choices=[9600, 57600, 115200], default=config.init_serial.baud, 
        help=f"baud rate for device (D: {config.init_serial.baud})")
    
    serial_settings.add_argument("data", nargs="?", type=int, action="store",
        choices=[6, 7, 8], default=config.init_serial.data_bits, 
        help=f"number of data bits (D: {config.init_serial.data_bits})")
    
    serial_settings.add_argument("stop", nargs="?", type=int, action="store",
        choices=[1, 2], default=config.init_serial.stop_bits, 
        help=f"number of stop bits (D: {config.init_serial.stop_bits})")
    
    serial_settings.add_argument("parity", nargs="?", type=str, action="store",
        choices=["Y", "N"], default=config.init_serial.parity,
        help=f"whether parity is enabled (D: \"{config.init_serial.parity}\")")
    
    # Mode select
    parser.add_argument("-m", "--mode", nargs="?", action="store", default="dumb",
        type=str, choices=["dumb", "local"], 
        help="""mode to start the monitor in dumb or local(-line) 
        (D: \"dumb\")""")
    
    # Non printable char display toggle
    parser.add_argument("-d", "--display", action="store_true", 
        default=False, help="enable the printing of non-printable chars")
    
    # # Print in byte formula
    # parser.add_argument("-a", "--all", action="store_true", default=False,
    #     help="enable printing of all chars as bytes")

    return parser