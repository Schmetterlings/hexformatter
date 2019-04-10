#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
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


def format_frame_info(hex):
    """
    Converts hex to binary and gets data from bits.

    :param hex: 2 character string
    :return: string
    """
    info = ""
    binary = bin(int(hex, 16))[2:].zfill(8)

    frame_length = int(binary[:4], 2)
    print (frame_length)

    frame_type = int(binary[6:7])
    if frame_type == 0:
        type = "RTR"
    else:
        type = "DATA"

    id_type = int(binary[7:8])
    if id_type == 0:
        idtype = "AVR"
    else:
        idtype = "STD"
    frame_info = (frame_length, type, idtype)
    return frame_info



def format_frame_id(hex):
    """
    Converts hex to binary and gets frame id.

    :param hex: 4 character string
    :return: string
    """
    binary = (bin(int(hex, 16))[2:].zfill(16))[:11]

    return int(binary, 2)

def format_frame_data(hex):

    binary = (bin(int(hex, 16))[2:].zfill(16))[:11]

    return int(binary, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format and display information from raw SD card file.")
    parser.add_argument("file", help="Path to raw SD card file.")
    args = parser.parse_args()

    frame_list = format_file(args.file)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Telemetry.xlsx')
    worksheet = workbook.add_worksheet()

    # 1st row: headers
    headers = ('Time[ms]','Length','Frame type','ID Type','ID','Data')

    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for name in (headers):
        worksheet.write(row, col, name)
        col += 1

    col = 0
    row += 1


    for frame in frame_list:
        frame_arrival_time = int(frame[3] + frame[2] + frame[1] + frame[0], 16)

        worksheet.write(row, col, frame_arrival_time)
        col += 1


        frame_info = format_frame_info(frame[4])
        worksheet.write(row, col, frame_info[0])
        col += 1
        worksheet.write(row, col, frame_info[1])
        col += 1
        worksheet.write(row, col, frame_info[2])
        col += 1
        worksheet.write(row, col, format_frame_id(frame[6] + frame[5]))

        col += 1
        if frame_info[0] > 0:
            id = frame[7]
            if frame_info[0] > 1:
                pass
                for c in frame[8:]:
                    id += c
            worksheet.write(row, col, format_frame_data(id))

        col = 0
        row +=1
    workbook.close()
