.globl _start
.globl main
.globl _exit
.weak _exit

.text

_start:
    # clear bss
    nop
    li	  sp,0x100
    addi  sp,sp,-32
    sw	  s0,24(sp)
    li	  a5,1
    sw	  a5,-20(s0)
    li	  a5,10
    sw	  a5,-24(s0)
    
    lw	  a4,-20(s0)
    lw	  a5,-24(s0)
    add   a5,a5,a4



    jal     main
    j       _exit

_exit:
    j _exit
// end of crt.S
