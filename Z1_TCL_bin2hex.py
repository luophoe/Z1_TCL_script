# Z1_TCL_bin2hex.py
#
# Created on: 12/08/2021
#     Author: Anyka
#      		  Phoebe Luo
import os
import sys


# ---------------------------------------------------Part 1. Functions--------------------------------------------------
# Function 1. turn decimal into 32 bit hex address
def getaddr(line_addr):
    # if the line_addr is 0 and int cannot process
    if line_addr == "0":
        line_hex = "00000000"
    else:
        line_hex = str(hex(int(line_addr, 10)))[2:]
        # if the transformed hex number has missing 0's
        if len(line_hex) < 8:
            num = 8 - len(line_hex)
            for i in range(num):
                line_hex = "0" + line_hex
                
    return line_hex


# Main Function. to turn binary file to hex file
def bin2hex(bin_file, hex_file):
    # if the hex file is in the format with no address
    line_num = 0
    if file_format == "1":
        bin_file = open(bin_file, "rb")
        hex_file = open(hex_file, "w+")
        byte = bin_file.read(1)
        write_string = ""

        while byte:
            data = ord(byte)
            string = "%02x" % (data)
            write_string = string + write_string
            if len(write_string) == 8:
                hex_file.write(write_string + "\n")
                write_string = ""
            byte = bin_file.read(1)
        bin_file.close()
        hex_file.close()
    # if the hex file is in the format with address
    elif file_format == "0":
        bin_file = open(bin_file, "rb")
        hex_file = open(hex_file, "w+")
        byte = bin_file.read(1)
        write_string = ""
        line_addr = "0"

        while byte:
            data = ord(byte)
            string = "%02x" % (data)
            write_string = string + write_string
            if len(write_string) == 8:
                fin_addr = get_addr(line_addr)
                hex_file.write(‘@" + fin_addr + "   " + write_string + "\n")
                write_string = ""
                # if the line_addr is 0 and int cannot process
                if line_addr == "0":
                    line_addr = "4"
                else:
                    line_addr = str(int(line_addr) + 4)
            byte = bin_file.read(1)
        bin_file.close()
        hex_file.close()
                               
    return line_num


# ----------------------------------------------------Part 2. Main------------------------------------------------------
# call bin2hex
# bin2hex(bin_file, hex_file)
line = bin2hex(sys.argv[1], sys.argv[2], sys.argv[3])
print("hex file " + sys.argv[2] + " updated.")
print("total line: " + str(line))
