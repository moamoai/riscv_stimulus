.globl _start
.globl main
.globl _exit
.weak _exit

.text

_start:
    # clear bss
    nop
    jal     main
    j       _exit

_exit:
    j _exit
// end of crt.S
