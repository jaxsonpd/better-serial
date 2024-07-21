## 
# @file utils.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-07-22
# @brief This file contains various helper functions for the project

import threading
import datetime

def close_com_threads():
    """
    Close all serial port related threads using their name. This is not
    the best way to do this but I can't think of a better one right now.
    """
    com_thread_names = ["com_rx_thread", "com_tx_thread"]

    for thread in threading.enumerate():
        if (thread.getName() in com_thread_names):
            thread.stop()


def get_time_str() -> str:
    """
    Get the current time and return it as a str to append at the start of
    system messages.

    ### Returns:
    out : str
        Print string
    """
    now = datetime.datetime.now()

    return now.strftime("[%H:%M:%S]:")

