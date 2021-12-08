# Z1_TCL_bin2hex.py
#
# Created on: 12/08/2021
#     Author: Anyka
#      		  Phoebe Luo
import os
import sys


# ---------------------------------------------------Part 1. Functions--------------------------------------------------
# Main Function. to turn binary file to hex file
def bin2hex(bin_file, hex_file):
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


# ----------------------------------------------------Part 2. Main------------------------------------------------------
# call bin2hex
# bin2hex(bin_file, hex_file)
bin2hex(sys.argv[1], sys.argv[2])
print("hex file " + sys.argv[2] + " updated.")
