#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys


def format_file(filename):
    """
    Open and format the file as list containing only important chunks of hex values.

    :param filename: filename string
    :returns: 2D list
    """
    with open(filename, "rb") as file:
        hex_list = ['{:02X}'.format(c) for c in file.read()]

    formatted_list = []
    last_id = 2  # Omit the header bytes

    for idx, _ in enumerate(hex_list):
        if hex_list[idx] == "CC":
            if hex_list[idx+1] == "DD":
                # Append hex to list omitting the header and footer values
                formatted_list.append(hex_list[last_id:idx])
                last_id = idx+4

    return formatted_list


def format_frame_info(hex):
    """
    Converts hex to binary and gets data from bits.

    :param hex: 2 character string
    :return: string
    """
    info = ""
    binary = bin(int(hex, 16))[2:].zfill(8)

    frame_length = int(binary[:4], 2)
    info += "Frame length: {}\n".format(frame_length)

    frame_type = int(binary[6:7])
    if frame_type == 0:
        info += "Frame type: RTR\n"
    else:
        info += "Frame type: DATA\n"

    id_type = int(binary[7:8])
    if id_type == 0:
        info += "ID type: AVR\n"
    else:
        info += "ID type: STD\n"

    return info


def format_frame_id(hex):
    """
    Converts hex to binary and gets frame id.

    :param hex: 4 character string
    :return: string
    """
    binary = (bin(int(hex, 16))[2:].zfill(16))[:11]

    return "Frame ID: {}".format(int(binary, 2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format and display information from raw SD card file.")
    parser.add_argument("file", help="Path to raw SD card file.")
    args = parser.parse_args()

    frame_list = format_file(args.file)

    for frame in frame_list:
        frame_arrival_time = int(frame[3] + frame[2] + frame[1] + frame[0], 16)

        print(format_frame_info(frame[4]))
        print(format_frame_id(frame[6] + frame[5]))

        print("Frame arrival: {} [ms]".format(frame_arrival_time))
