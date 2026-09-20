;framebuffer.asm

section .text
    global framebuffer_init

framebuffer_init:

    mov rax, 0xA0000

    ret
