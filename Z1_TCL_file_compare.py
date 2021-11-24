# Z1_TCL_file_compare.py
#
# Created on: 11/11/2021
#     Author: Anyka
#             Phoebe Luo
import re
import os
import sys
import linecache

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


# Main Function. compare the lines in ref_file and the result and output result to comp_result_file
def file_compare(ref_file, result_file, comp_result_file):
    # 1. print and write into file to identify the start of a comaprison
    # get the file name for ref_file and result_file for printing
    ref_file_name = ref_file.split("/")[-1]
    result_file_name = result_file.split("/")[-1]
    # print
    print("===========================================================================================================")
    print("The ref file: " + ref_file_name + " and result file: " + result_file_name + " compare start!")
    # write into file
    # open the comp_result_file so that output can be written into it
    file = open(comp_result_file, "a+")
    file.write("===========================================================================================================")
    file.write("The ref file: " + ref_file_name + " and result file: " + result_file_name + " compare start!")

    # keep track of the line number
    line_num = 0
    # identify if the comparison failed
    comp_failed = 0

    for line_ref in open(ref_file, "r"):
        # 2. get rid of the extra content
        line_ref = stripextra(line_ref)

        # 3. get the corresponding line from the result_file
        # get the raw line in result_file
        line_result = linecache.getline(result_file, line_num + 1)
        # get rid of the extra content
        line_result = stripextra(line_result)

        # 5. check if the lines are identical
        if line_ref != line_result:
            print("i = " + str(line_num + 1) + ", ref = " + line_ref + ", redsult = " + line_result + ", the compare failed!")
            # write into comp_result_file
            file.write("i = " + str(line_num + 1) + ", ref = " + line_ref + ", redsult = " + line_result + ", the compare failed!")
            comp_failed = 1
        else:
            print("i = " + str(line_num + 1) + ", ref = " + line_ref + ", redsult = " + line_result + ", the compare passed!")
            # write into comp_result_file
            file.write("i = " + str(line_num + 1) + ", ref = " + line_ref + ", redsult = " + line_result + ", the compare passed!")

        # update the line number
        line_num += 1
    file.write("\n")

    # 7. check if the line number is the same
    # count line number for ref_file
    line_num_ref = 0
    for line_num_ref, line in enumerate(open(ref_file, "r")):
        pass
    line_num_ref += 1
    # count line number for result file
    line_num_result = 0
    for line_num_result, line in enumerate(open(result_file, "r")):
        pass
    line_num_result += 1
    # compare the line number
    if line_num_ref != line_num_result:
        # warning message printing
        print("Warning: The ref file: " + ref_file_name + " and result file: " + result_file_name + " line number is different! (ref file: " + str(line_num_ref + 1) + ", result file: " + str(line_num_result + 1) + ")")
        # write into comp_result_file
        file.write("Warning: The ref file: " + ref_file_name + " and result file: " + result_file_name + " line number is different! (ref file: " + str(line_num_ref + 1) + ", result file: " + str(line_num_result + 1) + ")")

    # 8. check if the comparison passed
    if comp_failed == 0:
        # comparison passed
        print("The ref file: " + ref_file_name + " and result file: " + result_file_name + " compare passed!")
        # write into comp_result_file
        file.write("The ref file: " + ref_file_name + " and result file: " + result_file_name + " compare passed!")

    elif comp_failed == 1:
        # comparison failed
        print("The ref file: " + ref_file_name + " and result file: " + result_file_name + " compare failed!")
        # write into comp_result_file
        file.write("The ref file: " + ref_file_name + " and result file: " + result_file_name + " compare failed!")


# -----------------------------------------------------Part 2. Main-----------------------------------------------------
# call file_compare
# file_compare(ref_file, result_file, comp_result_file)
file_compare(sys.argv[1], sys.argv[2], sys.argv[3])
