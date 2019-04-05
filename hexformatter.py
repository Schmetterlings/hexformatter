#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


def format_file(filename):
    """
    Open and format the file as list containing only important chunks of hex values.

    :param filename: filename string
    :returns: 2D list
    """
    with open(filename, "rb") as file:
        hex_list = ['{:02X}'.format(c) for c in file.read()]

    formatted_list = []
    last_id = 2  # Omit the header bits

    for idx, _ in enumerate(hex_list):
        if hex_list[idx] == "CC":
            if hex_list[idx+1] == "DD":
                # Append hex to list omitting the header and footer values
                formatted_list.append(hex_list[last_id:idx])
                last_id = idx+4

    return formatted_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format and display information from raw SD card file.")
    parser.add_argument("file", help="Path to raw SD card file.")
    args = parser.parse_args()

    print(format_file(args.file))
