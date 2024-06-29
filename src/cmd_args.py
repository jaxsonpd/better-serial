## 
# @file cmd_args.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-06-29
# @brief Provides functionality to parse the command line arguments

import argparse

def setup_cmd_args() -> argparse.ArgumentParser:
    """
    Setup the command line arguments that can be provided to the program
    """
    parser = argparse.ArgumentParser(
        description="A simple serial monitoring application.")
    
    # Serial port settings
    serial_settings = parser.add_argument_group("Port Settings",
        "Serial port settings")
    
    serial_settings.add_argument("port", nargs="?", type=str, action="store",
        default="/dev/ttyUSB0", help="port to open (D: /dev/ttyUSB0)")
    
    serial_settings.add_argument("data", nargs="?", type=int, action="store",
        choices=[6, 7, 8], default=8, help="number of data bits (D: 8)")
    
    serial_settings.add_argument("stop", nargs="?", type=int, action="store",
        choices=[1, 2], default=1, help="number of stop bits (D: 1)")
    
    serial_settings.add_argument("baud", nargs="?", type=int, action="store",
        choices=[9600, 57600, 115200], default=9600, 
        help="baud rate for device (D: 9600)")
    
    serial_settings.add_argument("parity", nargs="?", type=str, action="store",
        choices=["Y", "N"], default="N",
        help="whether parity is enabled \"y/n\" (D: \"n\")")
    
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