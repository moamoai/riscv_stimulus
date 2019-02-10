#!/bin/sh -e

# TEST_ELF= ../../riscv-tests/isa/rv32ui-p-add
# TEST_ELF= ../../riscv-tests/isa/rv32ui-p-add.dump

TEST_DIR=../../riscv-tests/isa/
TEST_ELF=$1

if [ ! -f ${TEST_DIR}${TEST_ELF} ]; then
  echo "Error no file ${TEST_DIR}${TEST_ELF}"
  exit
else 
  if [ -f ${TEST_DIR}${TEST_ELF}.dump ]; then
    /bin/cp ${TEST_DIR}${TEST_ELF}.dump .
    FAIL_ADDR=`grep "<fail>:" ${TEST_ELF}.dump | awk '{print $1}'`
    PASS_ADDR=`grep "<pass>:" ${TEST_ELF}.dump | awk '{print $1}'`
    echo ${PASS_ADDR}
    echo ${FAIL_ADDR}
  else
    exit
  fi
fi

# riscv64-unknown-elf-objcopy -O verilog ${TEST_ELF} test.hex
# riscv64-unknown-elf-objcopy -O ihex ${TEST_ELF} test.hex
riscv64-unknown-elf-objcopy --reverse-bytes=4 -O  binary ${TEST_DIR}${TEST_ELF} test.bin
xxd -ps -c 4 test.bin > test_4B.hex
# xxd -ps -c 4  test.hex > test_4B.hex
# elf2hex 4 8192 ${TEST_ELF} > test_4B.hex

if [ ! -d ./log ]; then
  mkdir -p log
fi

python3.7 riscv_sim.py ./test_4B.hex ${PASS_ADDR} ${FAIL_ADDR} > log/${TEST_ELF}.log
# if [ $? -e 1 ]
#   echo "Pass"
# else
#   echo "Fail"
# fi

