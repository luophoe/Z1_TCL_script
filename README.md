# Z1_TCL_script
- when the chip system uses MEMC module to access outside memory, the system address will be transformed into memory address with a different format, the 32 bit address is in the format of:  
  
W_addr_default = excess_zeros(5) + bank_width(3) + row_width(13) + col_width(11)
i.e. 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0   
mem_addr_default = excess_zeros(5) + row_width (3:1) + bank_width(3) + row_width(13:4) + col_width(11)
i.e. 31 30 29 28 27 13 12 11 26 25 24 23 22 21 20 19 18 17 16 15 14 10 9 8 7 6 5 4 3 2 1 0
  
- when the address change, the continuous system data that is store will become incontinuous and scattered memory data, so the loading and the accessing data will be difficult without thehelp of a script
  
- two scripts are required: 
   
Z1_TCL_get_data.py "download_file" "start_addr" data_byte_length "result_file" data_format bank_width row_width col_width
Z1_TCL_put_data.py "src_file" src_format "upload_file" "start_addr" bank_width row_width col_width
  
- NOTES:   
  
the memory data file is 320.00 MB so functionality must be compatible with large file processing with high speed;  
the multiple format of the system files must be compatible  
