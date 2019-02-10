#!/usr/bin/env python
# coding: utf-8
#

import sys

filepath  = sys.argv[1]
PASS_ADDR = int(sys.argv[2][2:], 16)
FAIL_ADDR = int(sys.argv[3][2:], 16)
pc      = 0
# pc      = 0x100

print("filepath: {0}".format(filepath))
print("PASS_ADDR: 0x{0:08x}".format(PASS_ADDR))
print("FAIL_ADDR: 0x{0:08x}".format(FAIL_ADDR))

DUMP_REG_NUM = 0x20
cb_flag = 0
x_r = [0] * 32 # x0->x31
DMEM_DIR = {}
CSR_DIR = { 0x0f14: 0x0 }

############
# INPUT Inst
#############
inst_list_4B = []
with open(filepath) as fp:
   line = fp.readline()
   while line:
     inst_list_4B.append(line.strip())
     line = fp.readline()

# # for line in sys.stdin:
#    inst_list_4B.append(line.strip())


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

# DUMP_LIST=range(0, DUMP_REG_NUM)
DUMP_LIST=list(range(0, 8)) + list(range(28, 32))
# print(DUMP_LIST)

for i in DUMP_LIST:
  print("{0:10}".format("x"+str(i)), end="", file=f_regtrace)
print("", file=f_regtrace)

def dump_registers():
  print("{0:04x} ".format(pc), end="", file=f_regtrace)
  for i in DUMP_LIST:
    print("{0:08x}  ".format(x_r[i]), end="", file=f_regtrace)
    # x{0:4}: 0x{1:08x}".format(i, x_r[i], pc*4))
  print("", file=f_regtrace)

def dump_dmem():
  # print("")
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

BEQ   = (lambda x,y: x==y)
BNE   = (lambda x,y: x!=y)
BLT   = (lambda x,y: x<y)
BGE   = (lambda x,y: x>=y)
BLTU  = (lambda x,y: x<y)
BGEU  = (lambda x,y: x>y)
func3_CB_LIST = [BEQ, BNE,  "",   "", BLT, BGE, BLTU, BGEU]

def get_compllement(data, bit_num):
  if(imm1_s == 1):
    complement = -((~imm1 & 0x7FF) + 1)
  # if(data >= (1<<(bit_num-1))):
  #   complement = (data - (1<<(bit_num-1))) * -1
  # else:
  #   complement = data
  return complement
  
op = ""
for time in range(1, 0x800):
  inst   = bin_list_4B[int(pc/4)]
  opcode = get_opcode(inst)
  rd      = get_bit(inst, 11,  7) 
  rs1     = get_bit(inst, 19, 15) 
  rs2   = get_bit(inst, 24, 20) 
  # 0010011['ADDI', 'SLTI', 'SLTIU', 'XORI', 'ORI', 'ANDI', 'SLLI', 'SRLI', 'SRAI']
  if   opcode == 0b0010011:
    func3   = get_bit(inst, 14, 12) 
    imm1    = get_bit(inst, 30, 20) 
    imm1_s  = get_bit(inst, 31, 31) 
    # print("pc  : 0x{0:08x}".format(pc));
    # print("imm1      : 0d{0}".format(imm1));
    # imm1 = get_compllement(imm1, 12)
    if(imm1_s == 1):
      imm1 = -((~imm1 & 0x7FF) + 1)
    x_r[rd] = func3_OP_LIST[func3](x_r[rs1], imm1) & 0xFFFFFFFF
    print("pc:0x{1:04x} func3:{5} x_r[{2:04x}]: 0x{4:08x} rs1: {3:02d} imm1: 0x{0:08x} ".format(imm1, pc, rd, rs1, x_r[rd], func3));
  # 0100011['SB', 'SH', 'SW']
  elif opcode == 0b0100011:
    imm   = get_bit(inst, 11,  7) 
    func3 = get_bit(inst, 14, 12) 
    imm   = (get_bit(inst, 31, 25)<<5) + imm
    DMEM_DIR[x_r[rs1]+imm] = x_r[rs2]
  # 0000011['LB', 'LH', 'LW', 'LBU', 'LHU']
  elif opcode == 0b0000011:
    imm   = get_bit(inst, 11,  7) 
    func3 = get_bit(inst, 14, 12) 
    imm   = get_bit(inst, 31, 20) 
    x_r[rd] = DMEM_DIR[x_r[rs1]+imm]
  # 0110011['ADD', 'SUB', 'SLL', 'SLT', 'SLTU', 'XOR', 'SRL', 'SRA', 'OR', 'AND']
  elif opcode == 0b0110011:
    func3 = get_bit(inst, 14, 12) 
    func7 = get_bit(inst, 31, 25) 
    x_r[rd] = func3_OP_LIST[func3](x_r[rs1], x_r[rs2]) & 0xFFFFFFFF
  # 1101111['JAL']
  elif opcode == 0b1101111:
    imm19_12 = get_bit(inst, 19, 12) 
    imm11    = get_bit(inst, 20, 20) 
    imm10_01 = get_bit(inst, 30, 21) 
    imm20    = get_bit(inst, 31, 31) 
    imm = (imm20<<20) + (imm10_01<<1) + (imm11<<11) + (imm19_12<<12)
    if(rd!=0):
      x_r[rd] = pc + 4
    op = "jal"
    if(imm20 == 1):
      imm = -((~imm & 0x7FFF) + 1)
  # 0110111['LUI']
  elif opcode == 0b0110111:
    imm_31_12 = get_bit(inst, 31, 12) 
    x_r[rd] = (imm_31_12<<12)
  # 1110011['ECALL', 'EBREAK', 'CSRRW', 'CSRRS', 'CSRRC', 'CSRRWI', 'CSRRSI', 'CSRRCI']
  elif opcode == 0b1110011:
    csr    = get_bit(inst, 31, 20) 
    funct3 = get_bit(inst, 14, 12) 
    print("funct3: {0}".format(funct3))
    if  (funct3==1):
      CSR_DIR[csr] = x_r[rs1]
    elif(funct3==2):
      if csr in CSR_DIR:
        pass
      else:
        print("ERROR NO CSR: 0x{0:04x} pc:{1:04x}".format(csr, pc))
        exit()
      x_r[rd] = CSR_DIR[csr]
    elif(funct3==3):
      x_r[rd] = CSR_DIR[csr]
    # x_r[rd] = 4
  # 1100011['BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU']
  elif opcode == 0b1100011:
    func = get_bit(inst, 14, 12) 
    imm_4_1   = get_bit(inst, 11, 8) 
    imm_11    = get_bit(inst, 7, 7) 
    imm_10_5  = get_bit(inst, 30, 25) 
    imm_12    = get_bit(inst, 31, 31) 
    imm =  (imm_4_1  <<  1) \
         + (imm_11   << 11) \
         + (imm_10_5 <<  5) \
         + (imm_12   << 12) 
    cb_flag = func3_CB_LIST[func](x_r[rs1], x_r[rs2])
    if(imm_12 == 1):
      imm = -((~imm & 0x7FF) + 1)
    # print("# func: {0} cb_flag: {1} xrs1: {2} xrs2: {3}".format(func, cb_flag, x_r[rs1], x_r[rs2]))
  # 0010111['AUIPC']
  elif opcode == 0b0010111:
    pass
  # 0001111['FENCE', 'FENCE.I']
  elif opcode == 0b0001111:
    pass
  else:
    print("ERROR no opcode")
    print("pc: 0x{0:08x}".format(pc))
    print("opcode: 0b{0:07b}".format(opcode))
    exit()

  # dump_dmem();
  dump_registers()
  if   pc == PASS_ADDR:
    print("Pass")
    exit(1)
  elif pc == FAIL_ADDR:
    print("Fail")
    exit(0)
  elif op == "jal":
    pc      = pc + imm
  elif(cb_flag):
    # print("# BRANCH")
    pc = pc + imm
    cb_flag = 0
  else:
    pc += 4
  op = ""

print("pc: 0x{0:08x}".format(pc))

f_regtrace.close()
