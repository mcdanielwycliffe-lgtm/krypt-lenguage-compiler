;main.asm
BITS 32

global _start
extern kernel

section .text

_start:
    cli

    mov esp, stack32_top

    mov eax, cr4
    or eax, 0x20
    mov cr4, eax

    call setup_page_tables

    mov eax, pml4_table
    mov cr3, eax

    mov ecx, 0xC0000080
    rdmsr
    or eax, 0x100
    wrmsr

    mov eax, cr0
    or eax, 0x80000000
    mov cr0, eax

    lgdt [gdt64_descriptor]

    jmp 0x08:long_mode_entry

setup_page_tables:
    mov edi, pml4_table
    mov eax, 0
    mov ecx, 4096
    rep stosb

    mov edi, pdpt_table
    mov eax, 0
    mov ecx, 4096
    rep stosb

    mov edi, pd0_table
    mov eax, 0
    mov ecx, 4096
    rep stosb

    mov edi, pd1_table
    mov eax, 0
    mov ecx, 4096
    rep stosb

    mov edi, pd2_table
    mov eax, 0
    mov ecx, 4096
    rep stosb

    mov edi, pd3_table
    mov eax, 0
    mov ecx, 4096
    rep stosb

    mov dword [pml4_table], pdpt_table
    or dword [pml4_table], 0x03

    mov dword [pdpt_table], pd0_table
    or dword [pdpt_table], 0x03

    mov dword [pdpt_table + 8], pd1_table
    or dword [pdpt_table + 8], 0x03

    mov dword [pdpt_table + 16], pd2_table
    or dword [pdpt_table + 16], 0x03

    mov dword [pdpt_table + 24], pd3_table
    or dword [pdpt_table + 24], 0x03

    mov edi, pd0_table
    mov eax, 0
    call fill_page_directory

    mov edi, pd1_table
    mov eax, 0x40000000
    call fill_page_directory

    mov edi, pd2_table
    mov eax, 0x80000000
    call fill_page_directory

    mov edi, pd3_table
    mov eax, 0xC0000000
    call fill_page_directory

    ret

fill_page_directory:
    mov ecx, 512

.fill:
    mov edx, eax
    or edx, 0x83

    mov [edi], edx
    mov dword [edi + 4], 0

    add eax, 0x200000
    add edi, 8

    loop .fill

    ret

BITS 64

long_mode_entry:
    mov ax, 0x10
    mov ds, ax
    mov es, ax
    mov ss, ax

    mov rsp, stack64_top
    and rsp, -16

    mov edi, ebx

    call kernel

hang:
    cli
    hlt
    jmp hang

section .data
align 8

gdt64:
    dq 0x0000000000000000
    dq 0x00AF9A000000FFFF
    dq 0x00AF92000000FFFF

gdt64_descriptor:
    dw gdt64_descriptor - gdt64 - 1
    dq gdt64

section .bss
align 4096

pml4_table:
    resq 512

pdpt_table:
    resq 512

pd0_table:
    resq 512

pd1_table:
    resq 512

pd2_table:
    resq 512

pd3_table:
    resq 512

align 16

stack64:
    resb 16384

stack64_top:

align 16

stack32:
    resb 4096

stack32_top: