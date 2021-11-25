# Z1_TCL_data_format_trans.py
#
# Created on: 11/11/2021
#     Author: Anyka
#             Phoebe Luo
import re
import os
import sys


# ---------------------------------------------------Part 1. Functions--------------------------------------------------
# Function 1. strip the extra enters, tabs, and spaces
def stripextra(line):
    # strip the extra strings
    line = line.replace(" ", "")
    line = line.replace("\r", "")
    line = line.replace("\t", "")
    line = line.replace("\n", "")

    # if extra strings still exists, strip again by recursively calling
    if line.find(" ") >= 0 or line.find("\r") >= 0 or line.find("\t") >= 0 or line.find("\n") >= 0:
        stripextra(line)
    else:
        return line


# Main Function. identify the transition required, extract data from src_file, and perform the transition to put into result_file
def data_format_trans(src_file, result_file, trans_type):
    # strip_line for keeping track of the line to go into result file
    string_line = ""
    # count for keeping track of the number of lines that are added to string_line
    count = 0
    # open the result_file for writing
    file = open(result_file, "w+")

    for line in open(src_file, "r"):
        if trans_type == "1t2":
            # 1. turn file from 1 byte per row to 2 byte per row
            line = line[0:2]
            line = stripextra(line)
            # if the string_line already has 2 byte in it
            if count == 2:
                # write it into result file
                file.write(string_line)
                file.write("\n")
                # update teh line to the current line
                string_line = line
                # change count to 1
                count = 1
            # if the string_line does not have 2 byte in it yet
            else:
                # update the line to concat the current line
                string_line = line + string_line
                # update count
                count += 1

        elif trans_type == "1t4":
            # 2. turn file from 1 byte per row to 4 byte per row
            line = line[0:2]
            line = stripextra(line)
            # if the string_line already has 4 byte in it
            if count == 4:
                # write it into result file
                file.write(string_line)
                file.write("\n")
                # update the line to the current line
                string_line = line
                # change count to 1
                count = 1
            # if the string_line does not have 2 byte in it yet
            else:
                # update the line to concat the current line
                string_line = line + string_line
                # update count
                count += 1

        elif trans_type == "2t1":
            # 3. turn file from 2 byte per row to 1 byte per row
            line = line[0:5]
            line = stripextra(line)
            file.write(line[2:4])
            file.write("\n")
            file.write(line[0:2])
            file.write("\n")

        elif trans_type == "2t4":
            # 4. turn file from 2 byte per row to 4 byte per row
            line = line[0:5]
            line = stripextra(line)
            # if the string already has 4 byte in it
            if count == 2:
                # write it into result file
                file.write(string_line)
                file.write("\n")
                # update the line to the current line
                string_line = line
                # change count to 1
                count = 1
            # if the string_line does not have 4 byte in it yet
            else:
                # update the line to concat the current line
                string_line = line + string_line
                # update count
                count += 1

        elif trans_type == "4t1":
            
