#!/usr/bin/env python
# coding: utf-8
#

# str = input()
# print(str)

import sys
opcode_dir={}
for line in sys.stdin:
   line = line.strip();
   line_list = line.split()
   opcode = line_list[-2]
   inst   = line_list[-1]
   if  opcode in opcode_dir:
     opcode_dir[opcode] += [inst]
   else:
     opcode_dir[opcode] = [inst]
   # print("{0:10s} {1}".format(opcode,inst)) 
for key in opcode_dir:
  print(key + str(opcode_dir[key]))

