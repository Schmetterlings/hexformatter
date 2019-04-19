#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
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

    frame_length = int(binary[:4], 2)

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


def find_id_name(frame_id):
    """
    Finds module name from frame id.

    :param frame_id: integer
    :return: tuple
    """
    textsplit = str(frame_id)
    fpart = textsplit[:2] + "00"
    spart = textsplit[2:]
    module_reason = ""
    module = ""

    with open("can_id.json") as file:
        data = json.load(file)
        for e in data["module_reason"]:
            if e["id"] == fpart:
                module_reason = e["name"]
                break

        for e in data["module"]:
            if e["id"] == spart:
                module = e["name"]
                break

    return (module_reason, module)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format and display information from raw SD card file.")
    parser.add_argument("file", help="Path to raw SD card file.")
    parser.add_argument("-m", "--mode", choices=["raw", "translated"], default="translated", help="Select which type of output you want.")
    parser.add_argument("-o", "--output", default="sd.csv", help="Path to output CSV file.")
    args = parser.parse_args()

    frame_list = format_file(args.file)

    # Create a CSV file
    with open(args.output, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)

        ###################
        # RAW OUTPUT FILE #
        ###################
        if args.mode == "raw":
            # Write headers to file
            headers = ('Czas [ms]', 'Długość', 'Typ ramki', 'Typ ID', 'ID', 'Dane [0]', 'Dane [1]', 'Dane [2]', 'Dane [3]', 'Dane [4]', 'Dane [5]', 'Dane [6]', 'Dane [7]')
            csvwriter.writerow(headers)

            # Iterate over the data and write it out row by row.
            for idx, frame in enumerate(frame_list):
                print("Writing frame [{}] to sheet...".format(idx))

                frame_time = int(frame[3] + frame[2] + frame[1] + frame[0], 16)
                frame_info = format_frame_info(frame[4])
                frame_id = format_frame_id(frame[6] + frame[5])

                # If length of frame data is available, convert hex to decimals and write them
                if frame_info[0] > 0:
                    frame_data = []

                    for x in range(frame_info[0]):
                        frame_data.append(int(frame[7+x], 16))
                    for x in range(frame_info[0] + 1, 9):
                        frame_data.append("-")

                    csvwriter.writerow([frame_time, frame_info[0], frame_info[1], frame_info[2], frame_id, 
                                        frame_data[0], frame_data[1], frame_data[2], frame_data[3], frame_data[4], frame_data[5], frame_data[6], frame_data[7]])

                else:
                    csvwriter.writerow([frame_time, frame_info[0], frame_info[1], frame_info[2], frame_id, 
                                        "-", "-", "-", "-", "-", "-", "-", "-"])

        ##########################
        # TRANSLATED OUTPUT FILE #
        ##########################
        else:
            print("Bartek tutaj wstaw swój kod.")
