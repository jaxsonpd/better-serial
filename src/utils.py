## 
# @file utils.py
# @author Jack Duignan (JackpDuignan@gmail.com)
# @date 2024-07-22
# @brief This file contains various helper functions for the project

import threading

def close_com_threads():
    """
    Close all serial port related threads using their name. This is not
    the best way to do this but I can't think of a better one right now.
    """
    com_thread_names = ["com_rx_thread", "com_tx_thread"]

    for thread in threading.enumerate():
        if (thread.getName() in com_thread_names):
            thread.