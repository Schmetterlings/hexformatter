# hexformatter

Formats and displays information from raw telemetry files.  
Uses files with proprietary *.spc* extension, strongly hardcoded.

## Order of data in bytes

1-4: Time [ms]  
5: Length, Frame type, ID type
  - Bit nr 0 -> ID Type
  - Bit nr 1 -> Frame Type
  - Bits nr 2, 3 -> Empty, reserved for future use
  - Bits nr 4, 5, 6, 7 -> Length of data

6: 1st part of frame ID (only bits nr 5, 6, 7 are used, the rest are empty)  
7: 2nd part of frame ID (all bits used)  
8: Data

## TODO:

[X] User chooses 1 of 2 modes for creating files (raw, translated)  
[X] Excel --> CSV  
[X] Enter raw converted (binary to decimal) data into column  
[ ] Compare time between frames (do not trust if longer than 20ms)  
[X] Create headers for all data frames  
[X] Fill adequate data frames with translated data  
