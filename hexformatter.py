#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import xlsxwriter


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


def format_frame_info(hexdata):
    """
    Converts hex to binary and gets data from bits.

    :param hexdata: 2 character string
    :return: tuple
    """
    binary = bin(int(hexdata, 16))[2:].zfill(8)

    data_length = ''.join(reversed(binary[:4]))
    frame_length = int(data_length, 2)

    frame_type = int(binary[6:7])
    if frame_type == 0:
        frametype = "RTR"
    else:
        frametype = "DATA"

    id_type = int(binary[7:8])
    if id_type == 0:
        idtype = "AVR"
    else:
        idtype = "STD"

    info = (frame_length, frametype, idtype)
    return info


def format_frame_id(hexdata):
    """
    Converts hex to binary and gets frame id.

    :param hexdata: 4 character string
    :return: integer
    """
    binary = (bin(int(hexdata, 16))[2:].zfill(16))[:11]

    return int(binary, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format and display information from raw SD card file.")
    parser.add_argument("file", help="Path to raw SD card file.")
    parser.add_argument("-o", "--output", default="sd.xlsx", help="Path to output Excel file.")
    args = parser.parse_args()

    frame_list = format_file(args.file)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(args.output)
    worksheet = workbook.add_worksheet()

    # Headers tuple
    headers = ('Time[ms]', 'Length', 'Frame type', 'ID Type', 'ID', 'Data')

    # Iterate over the data and write it out row by row.
    for idx, name in enumerate(headers):
        worksheet.write(0, idx, name)

    for idx, frame in enumerate(frame_list):
        frame_arrival_time = int(frame[3] + frame[2] + frame[1] + frame[0], 16)

        worksheet.write(idx+1, 0, frame_arrival_time)

        frame_info = format_frame_info(frame[4])
        worksheet.write(idx+1, 1, frame_info[0])
        worksheet.write(idx+1, 2, frame_info[1])
        worksheet.write(idx+1, 3, frame_info[2])
        worksheet.write(idx+1, 4, format_frame_id(frame[6] + frame[5]))

    workbook.close()
