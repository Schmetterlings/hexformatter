# hexformatter

Formats and displays information from raw telemetry files.  
Uses files with proprietary *.spc* extension, strongly hardcoded.

##Bits Names 
1.Time [h]
2.Time [m]
3.Time [s]
4.Time [ms]
5.Length, Frame type, ID type
  - Bits nr 7 to 4 -> Lenght
  - Bits nr 2,3 -> Empty
  - Bit nr 1 -> Frame Type
  - Bit nr 0 -> ID Type
6.1st part of frame ID(only 5,6,7 bit, rest empty)
7.2nd part o ID(all bits used)
8.Rest of frame is for data, based on length
