# Z1_TCL_put_data.py
#
# Created on: 11/05/2021
#     Author: Anyka
#      		  Phoebe Luo
import re
import os
import sys
import linecache
import os.path
from os import path


# --------------------------------------------------Part 1. Functions---------------------------------------------------
# Function 1. turn hex number into 32 bit binary string
def getbin(string, num):
    string_bin = str(bin(int(string, 16) + num))[2:]
    if len(string_bin) < 32:
        num = 32 - len(string_bin)
        for i in range(num):
            string_bin = "0" + string_bin
    return string_bin


# Function 2. turn system address into memory address format
def changeaddr(string, bank, row, col):
    # the new string will be in the order of string_zero + string_bank + string_row + string_col
    # string_zero is the non essential 0's that will not change
    string_zero = string[0:32 - bank - row - col]
    # string_row is the bank bits and the first part of the row bits that will become the new row bits
    string_row = string[32 - bank - row - col:32 - bank - row]
    # string_bank is the second part of the row bits that will become the new bank bits
    string_bank = string[32 - bank - row:32 - col]
    # string_col is the non essential row bits that will not change
    string_col = string[32-col:]

    new_string = string_zero + string_bank + string_row + string_col
    return new_string


# Function 3. strip the extra enters, tabs and spaces
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


# Main Function. put data to the memory file in the correct address line
def put_data(src_file, src_format, upload_file, start_addr, bank_width = 3, row_width = 13, col_width = 11):
    # 1. get data and its address from source file and put them into two lists
    list_data = []
    list_addr = []

    # if it is in the test_case format
    if src_format == 0:
        for line in open(src_file, "r"):
            line_list = line.split("\t")
            if line_list[0].find("//") >= 0:
                # this is a comment line
                continue
            # get the original address string and data string
            if line_list[0].find("@") >= 0:
                addr_orig = line_list[0]
                addr_orig = addr_orig[1:]
                data_orig = line_list[1]
                # split the string into data1, data2, data3, data4 from low address to high address
                data1 = data_orig[6:8]
                data2 = data_orig[4:6]
                data3 = data_orig[2:4]
                data4 = data_orig[0:2]
                list_data.append(data1)
                list_data.append(data2)
                list_data.append(data3)
                list_data.append(data4)
                # get the corrsponding address of the data in decimal
                data1_addr = getbin(addr_orig, 0)
                data2_addr = getbin(addr_orig, 1)
                data3_addr = getbin(addr_orig, 2)
                data4_addr = getbin(addr_orig, 3)
                list_addr.append(data1_addr)
                list_addr.append(data2_addr)
                list_addr.append(data3_addr)
                list_addr.append(data4_addr)

    # if it is in the format 1 format
    elif src_format == 1:
        # to keep track of the updating address
        addr_count = 0
        for line in open(src_file, "r"):
            # get the data string
            line = line[0:2]
            line = stripextra(line)
            list_data.append(line)
            # get the corresponding address of the data in decimal
            line_addr = getbin(start_addr, addr_count)
            addr_count = addr_count + 1
            list_addr.append(line_addr)

    # if it is in the format 2 format
    elif src_format == 2:
        # to keep track of the updating address
        addr_count = 0
        for line in open(src_file, "r"):
            # split the string into data1, data2, data3, data4 from low address to high address
            data1 = line[6:8]
            data2 = line[4:6]
            data3 = line[2:4]
            data4 = line[0:2]
            list_data.append(data1)
            list_data.append(data2)
            list_data.append(data3)
            list_data.append(data4)
            # get the corrsponding address of the data on decimal
            data1_addr = getbin(start_addr, 0 + addr_count)
            data2_addr = getbin(start_addr, 1 + addr_count)
            data3_addr = getbin(start_addr, 2 + addr_count)
            data4_addr = getbin(start_addr, 3 + addr_count)
            addr_count = addr_count + 4
            list_addr.append(data1_addr)
            list_addr.append(data2_addr)
            list_addr.append(data3_addr)
            list_addr.append(data4_addr)

    # 2. check if the upload file exist, and create an empty one filled with 0's if not
    if path.isfile(upload_file) == False:
        file = open(upload_file, "w+")
        # create a file with unit_nm_mem number of lines that are filled with 0000
        # unit number of the memory
        unit_num_mem = pow(2, (bank_width + row_width + col_width - 1))

        for i in range(unit_num_mem):
            file.write("0000\n")
        file.close()
        print("upload_file: " + upload_file + " created.")
        file = open(upload_file, "r+")
    else:
        file = open(upload_file, "r+")

    for i in range(len(list_data)):
        # 3. turn system address into memory address format
        sys_addr_bin = changeaddr(list_addr[i], bank_width, row_width, col_width)

        # 4. find the line number, the number for seek position, and high_low for upload_file
        # find the line number using the address
        line_data = int(sys_addr_bin, 2)/2
        # find the number for seek position
        seek_pos = line_data*5
        # identify if the higher byte or the lower byte should be changed
        is_high = int(sys_addr_bin, 2)%2

        # 5. write the data into file
        file.seek(seek_pos)
        line = file.readline(4)
        file.seek(seek_pos)
        if is_high == 1:
            file.write(list_data[i] + line[2:4])
        elif is_high == 0:
            file.write(line[0:2] + list_data[i])
    print("upload_file: " + upload_file + " updated.")


# ----------------------------------------------------Part 2. Main------------------------------------------------------
# call put_data
# put_data(src_file, src_format, upload_file, start_addr, bank_width, row_width, col_width)

# if the bank width, row width, and col width is defined, use the defined numbers
if len(sys.argv) == 8:
    put_data(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
# else if the bank width, row width, and col width is not defined, use the default numbers
else:
    put_data(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
