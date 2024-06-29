# better-serial

A serial terminal that isn't rubbish. This project was inspired by the
sorry state of the serial monitor offering available especially on windows.
I specifically was interested in the following features:

- Listing of available serial ports 
- Ability to change default configuration
- Terminal interface (no separate send box)
- Displaying of non visible ascii chars (this is my main gripe)
- Modern ish UI

## Installation

Clone the git repository and then run:

`
python3 ./src/main.py
`

This application has the following dependencies:

`
pyserial
`

## Use

There are two modes for this application. These are detailed in the following sections

### Dumb Terminal

In this mode the serial monitor acts like a dumb terminal sending chars when
pressed and writing chars when received. In this mode no special chars can be
sent to the device however the special char display switch for incoming data 
does work.

### Local Edit/CMD sender

In this mode the serial monitor has local line edit and allows the sending of 
special chars using the `\x00` method (where \ is a special char and must be
escaped). The terminal reads back as normal printing chars when they are
received.
