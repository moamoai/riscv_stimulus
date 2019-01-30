CCFLAGS=-nostartfiles -nostdlib \
# -static -std=gnu99 -fno-common -fno-builtin-printf \

LINK_LD=-T ./link.ld

default: all

all: comp dump hex

# ARCH=-march=rv64i -mabi=lp64
ARCH=-march=rv32i -mabi=ilp32
comp: hello.c _start.S
	riscv64-unknown-elf-gcc -g \
          ${ARCH}               \
          ${CCFLAGS}            \
          ${LINK_LD}            \
          -o hello.elf \
          _start.S hello.c

#riscv64-unknown-elf-gcc -O2 -o hello hello.c
dump:
	riscv64-unknown-elf-objdump -d -M intel -S hello.elf > hello.dump

hex: 
	riscv64-unknown-elf-objcopy -O verilog hello.elf hello.hex
	elf2hex 1 1024 ./hello.elf > hello_1B.hex
	elf2hex 4 256  ./hello.elf > hello_4B.hex

clean:
	rm -f *.o *.elf *.hex
