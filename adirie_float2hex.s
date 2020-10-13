    .data
avar: .float 3.45
hexhead: .asciiz "0x"


    .text
    .globl main
main:
    li $v0, 4
    la $a0, hexhead
    syscall
 la $s0, avar
 li $s2, 0xF
 li $s3, 8
 li $s4, 10
 l.s $f0, 0($s0)
 mfc1 $t1, $f0
printloop:
    move $t3, $t1 # move t1 into t3
    srl $t6, $t3, 28 # shift to the right to normalize
    and $t6, $t6, $s2 # use 0xF to mask
    slt $t4, $t6, $s4 # check if its less than 10
    beq $t4, $zero, hexletter
    addi $t6, $t6, 48
printing:
    move $a0, $t6
    li $v0, 11
    syscall
    sll $t1, $t1, 4
    addi $s3, $s3, -1
    bne $s3, $zero, loop1
    jr $ra
hexletter:
    addi $t6, $t6, 87
    j printing
ending:
li $v0, 10
syscall
 .end main