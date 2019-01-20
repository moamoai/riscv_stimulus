CCFLAGS=-nostartfiles -nostdlib \
# -static -std=gnu99 -fno-common -fno-builtin-printf \

LINK_LD=-T ./link.ld

default: all

all: comp dump hex

comp: hello.c _start.S
	riscv64-unknown-elf-gcc -g \
          ${CCFLAGS}            \
          ${LINK_LD}            \
          -o hello.elf \
          _start.S hello.c

#riscv64-unknown-elf-gcc -O2 -o hello hello.c
dump:
	riscv64-unknown-elf-objdump -d -M intel -S hello.elf

hex: 
	riscv64-unknown-elf-objcopy -O verilog hello.elf hello.hex

clean:
	rm -f *.o *.elf *.hex
