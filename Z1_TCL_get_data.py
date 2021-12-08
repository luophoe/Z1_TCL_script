# Z1_TCL_get_data.py
#
# Created on: 11/04/2021
#     Author: Anyka
#             Phoebe Luo
import re
import os
import sys
import linecache


# --------------------------------------------------Part 1. Functions---------------------------------------------------
# Function 1. turn hex number into 32 bit binary string
def getbin(string, num, bank_width, row_width, col_width):
    string_bin = str(bin(int(string, 16) + num))[2:]
    # 1. if the transformed binary number has missing 0's
    if len(string_bin) < 32:
        num = 32 - len(string_bin)
        for i in range(num):
            string_bin = "0" + string_bin
            
    # 2. if the transformed binary number has unnecessary 1's, change the bit to 0
    # unnecessary 1 on bit 31
    if string_bin[0] == "1":
        string_bin = "0" + string_bin[1:]
    # unnecessary 1 on bit 30
    if string_bin[1] == "1":
        string_bin = string_bin[0] + "0" + string_bin[2:]
    
    # 3. if the address has illegal bits, output a warning
    # calculate the appropreate length of the address
    addr_length = bank_width + row_widh + col_width
    # check if there is illegal number
    illegal_check = 0
    for num in string_bin[:32-addr_length]:
        if num != "0":
            illegal_check == 1
    if illegal_check == 1:
        print("Warning: illegal system address, access out of bound!")
    return string_bin


# Function 2. turn system address into memory address format
def chageaddr(string, bank, row, col):
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


# Main Function. get the data from the memory file and extract it from the correct address line
def get_data(download_file, start_addr, data_byte_len, result_file, data_format, bank_width = 3, row_width = 13, col_width = 11):
    # list_data to save all the data in the correct order
    list_data = []

    for i in range(0, data_byte_len):
        # 1. turn the hex address into binary
        start_addr_bin = getbin(start_addr, i, bank_width, row_width, col_width)

        # 2. turn system address into memory address format
        mem_addr_bin = changeaddr(start_addr_bin, bank_width, row_width, col_width)

        # 3. find line number and high_low for data extraction
        # find the line of the data
        line_data = int(mem_addr_bin, 2)/2
        # find the number for seek position
        seek_pos = line_data*5
        # identify if the whole line of the first line should be taken or only the higher byte
        is_high = int(mem_addr_bin, 2)%2

        # 4. find the data line and the corresponding byte
        file = open(download_file, "r+")
        file.seek(seek_pos)
        line = file.readline(4)
        if is_high == 1:
            line = line[0:2]
        else:
            line = line[2:4]
        list_data.append(line)

    # 5. write the data info file
    file = open(result_file, "w+")
    # write in format 1 with 1 byte per row
    if data_format == 0:
        for byte in list_data:
            file.write(byte + "\n")
    # write in format 2 with 4 bytes per row and in little endian representation
    elif data_format == 1:
        count = 0
        byte_string = ""
        for byte in list_data:
            byte_string = byte + byte_string
            count = count + 1
            if count == 4:
                file.write(byte_string + "\n")
                count = 0
                byte_string = ""
        if len(byte_string) != 0:
            file.write(byte_string)

    print("result_file: " + result_file + "updated.")

# -----------------------------------------------------Part 2. Main-----------------------------------------------------
# call get_data
# get_data(download_file, start_addr, data_byte_len, result_file, data_format, bank_width = 3, row_width = 13, col_width = 11)

# if the bank width, row width, and col width is defined, use the defined numbers
if len(sys.argv) == 9:
    get_data(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
# else if the bank width, row width, and col width is not defined, use the default numbers
else:
    get_data(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], int(sys.argv[5]))
