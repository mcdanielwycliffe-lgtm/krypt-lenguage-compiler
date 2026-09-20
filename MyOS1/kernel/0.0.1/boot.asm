;boot.asm

BITS 32

section .multiboot2
    align 8
multiboot2_header:
    dd 0xE85250D6
    dd 0
    dd multiboot2_header_end - multiboot2_header
    dd -(0xE85250D6 + 0 + (multiboot2_header_end - multiboot2_header))
    
    dw 0
    dw 0
    dd 8
multiboot2_header_end:
