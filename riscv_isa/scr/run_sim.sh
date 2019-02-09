#!/bin/sh -e

# TEST_ELF= ../../riscv-tests/isa/rv32ui-p-add
# TEST_ELF= ../../riscv-tests/isa/rv32ui-p-add.dump
TEST_ELF=../../riscv-tests/isa/$1

if [ ! -f ${TEST_ELF} ]; then
  echo "Error no file ${TEST_ELF}"
  exit
fi
if [ -f ${TEST_ELF}.dump ]; then
  /bin/cp ${TEST_ELF}.dump .
fi

# riscv64-unknown-elf-objcopy -O verilog ${TEST_ELF} test.hex
# riscv64-unknown-elf-objcopy -O ihex ${TEST_ELF} test.hex
riscv64-unknown-elf-objcopy --reverse-bytes=4 -O  binary ${TEST_ELF} test.bin
xxd -ps -c 4 test.bin > test_4B.hex
# xxd -ps -c 4  test.hex > test_4B.hex
# elf2hex 4 8192 ${TEST_ELF} > test_4B.hex

python3.7 riscv_sim.py
