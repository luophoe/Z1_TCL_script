# Z1_TCL_get_data.py
#
# Created on: 11/04/2021
#     Author: Anyka
#             Phoebe Luo
import re
import os
import sys
import linecache


# ------------------------------------------------------Part 1. Functions------------------------------------------------------
# Function 1. teurn hex number into 32 bit binary string
def getbin(string, num):
    string_bin = str(bin(int(string, 16) + num))[2:]
    if len(string_bin) < 32:
        num = 32 - len(string_bin)
        for i in range(num):
            string_bin = "0" + string_bin
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
