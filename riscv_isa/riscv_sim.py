#!/usr/bin/env python
# coding: utf-8
#

# str = input()
# print(str)

import sys

pc  = 0
x_r = [0] * 32 # x0->x31
DMEM_DIR = {}

############
# INPUT Inst
#############
inst_list_4B = []
for line in sys.stdin:
   inst_list_4B.append(line.strip())


#############
# PRINT DEBUG
#############
bin_list_4B = []
for i in range(0,len(inst_list_4B)):
  inst_hex = inst_list_4B[i]
  inst_bin = '{0:032b}'.format(int(inst_hex, 16))
  # print("0x{0} 0b{1}".format(inst_hex, inst_bin))
  bin_list_4B.append(inst_bin)


#############
# RISCV SIM
#############
def get_bit(inst, upper, lower):
  return int(inst[32-upper-1:32-lower], 2)
  
def get_opcode(inst):
  opcode = get_bit(inst, 6, 0)
  return opcode

f_regtrace = open('regtrace.txt', 'w')
print("{0:5}".format("pc"), end="", file=f_regtrace)
# for i in range(0, len(x_r)):
for i in range(0, 8):
  print("{0:10}".format("x"+str(i)), end="", file=f_regtrace)
print("", file=f_regtrace)

def dump_registers():
  print("{0:04x} ".format(pc), end="", file=f_regtrace)
  for i in range(0, 8):
    print("{0:08x}  ".format(x_r[i]), end="", file=f_regtrace)
    # x{0:4}: 0x{1:08x}".format(i, x_r[i], pc*4))
  print("", file=f_regtrace)

def dump_dmem():
  print("")
  for addr in DMEM_DIR:
    print("{0:08x} {1:08x}".format(addr, DMEM_DIR[addr]));


ADD  = (lambda x,y: x+y)
SLL  = (lambda x,y: x<<y)
SLT  = (lambda x,y: 1 if x<y else 0)
SLTI = (lambda x,y: 1 if x<y else 0)
XOR  = (lambda x,y: x^y)
SR   = (lambda x,y: x>>y)
OR   = (lambda x,y: x|y)
AND  = (lambda x,y: x&y)

func3_OP_LIST = [ADD, SLL, SLT, SLTI, XOR, SR, OR, AND]

def get_compllement(data, bit_num):
  if(data >= (1<<(bit_num-1))):
    complement = (data - (1<<(bit_num-1))) * -1
  else:
    complement = data
  return complement
  
op = ""
for time in range(1, 0x20):
  inst   = bin_list_4B[int(pc/4)]
  opcode = get_opcode(inst)
  # 0010011['ADDI', 'SLTI', 'SLTIU', 'XORI', 'ORI', 'ANDI', 'SLLI', 'SRLI', 'SRAI']
  if   opcode == 0b0010011:
    rd      = get_bit(inst, 11,  7) 
    func3   = get_bit(inst, 14, 12) 
    rs1     = get_bit(inst, 19, 15) 
    imm1    = get_bit(inst, 30, 20) 
    imm1_s  = get_bit(inst, 31, 31) 
    print("pc  : 0x{0:08x}".format(pc));
    print("imm1      : 0d{0}".format(imm1));
    # imm1 = get_compllement(imm1, 12)
    if(imm1_s == 1):
      imm1 = -((~imm1 & 0x7FF) + 1)
    print("imm1(comp): 0d{0}".format(imm1));
    
    x_r[rd] = func3_OP_LIST[func3](x_r[rs1], imm1)
  # 0100011['SB', 'SH', 'SW']
  elif opcode == 0b0100011:
    imm   = get_bit(inst, 11,  7) 
    func3 = get_bit(inst, 14, 12) 
    rs1   = get_bit(inst, 19, 15) 
    rs2   = get_bit(inst, 24, 20) 
    imm   = (get_bit(inst, 31, 25)<<5) + imm
    DMEM_DIR[x_r[rs1]+imm] = x_r[rs2]
  # 0000011['LB', 'LH', 'LW', 'LBU', 'LHU']
  elif opcode == 0b0000011:
    imm   = get_bit(inst, 11,  7) 
    func3 = get_bit(inst, 14, 12) 
    rs1   = get_bit(inst, 19, 15) 
    imm   = get_bit(inst, 31, 20) 
    x_r[rd] = DMEM_DIR[x_r[rs1]+imm]
  # 0110011['ADD', 'SUB', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'SRA', 'OR', 'AND']
  elif opcode == 0b0110011:
    rd    = get_bit(inst, 11,  7) 
    func3 = get_bit(inst, 14, 12) 
    rs1   = get_bit(inst, 19, 15) 
    rs2   = get_bit(inst, 24, 20) 
    func7 = get_bit(inst, 31, 25) 
    x_r[rd] = func3_OP_LIST[func3](x_r[rs1], x_r[rs2])
  # 1101111['JAL']
  elif opcode == 0b1101111:
    rd       = get_bit(inst, 11,  7) 
    imm19_12 = get_bit(inst, 19, 12) 
    imm11    = get_bit(inst, 20, 20) 
    imm10_01 = get_bit(inst, 30, 21) 
    imm20    = get_bit(inst, 31, 31) 
    imm = (imm20<<20) + (imm10_01<<1) + (imm11<<11) + (imm19_12<<12)
    x_r[rd] = pc + 4
    op = "jal"
  # 0110111['LUI']
  elif opcode == 0b0110111:
    rd        = get_bit(inst, 11,  7) 
    imm_31_12 = get_bit(inst, 31, 12) 
    x_r[rd] = (imm_31_12<<12)
  else:
    print("ERROR no opcode")
    print("pc: 0x{0:08x}".format(pc))
    print("opcode: 0b{0:07b}".format(opcode))
    exit()

  dump_dmem();
  dump_registers()
  if op == "jal":
    pc      = pc + imm
  else:
    pc += 4
  op = ""

print("pc: 0x{0:08x}".format(pc))

f_regtrace.close()
