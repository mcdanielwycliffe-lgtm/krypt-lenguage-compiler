//kernel.c
#include <stdint.h>
#include "../../declarations.h"
#include "../../framebuffer/framebuffer.c"
#include "../../font/font.c"

void PUTCHAR(
    const char word[9][17],
    int x,
    int y,
    uint32_t color
) {
    for (int line = 0; line < 9; line++) {
        for (int column = 0; column < 16; column++) {
            if (word[line][column] == '1') {
                put_pixel(
                    x + column,
                    y + line,
                    color
                );
            }
        }
    }
}

void PUTSTRING(
    const char* txt,
    int x,
    int y,
    uint32_t color
) {
    for (int i = 0; txt[i] != '\0'; i++) {
        if (txt[i] == 'A') {
            PUTCHAR(A, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'B') {
            PUTCHAR(B, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'C') {
            PUTCHAR(C, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'D') {
            PUTCHAR(D, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'E') {
            PUTCHAR(E, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'F') {
            PUTCHAR(F, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'G') {
            PUTCHAR(G, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'H') {
            PUTCHAR(H, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'I') {
            PUTCHAR(I, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'J') {
            PUTCHAR(J, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'K') {
            PUTCHAR(K, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'L') {
            PUTCHAR(L, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'M') {
            PUTCHAR(M, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'N') {
            PUTCHAR(N, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'O') {
            PUTCHAR(O, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'P') {
            PUTCHAR(P, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'Q') {
            PUTCHAR(Q, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'R') {
            PUTCHAR(R, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'S') {
            PUTCHAR(S, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'T') {
            PUTCHAR(T, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'U') {
            PUTCHAR(U, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'V') {
            PUTCHAR(V, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'W') {
            PUTCHAR(W, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'X') {
            PUTCHAR(X, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'Y') {
            PUTCHAR(Y, x, y, color);
            x += 26;
        }
        else if (txt[i] == 'Z') {
            PUTCHAR(Z, x, y, color);
            x += 26;
        }
        else if (txt[i] == ' ') {
            x += 26;
        }

        if (x + 16 >= (int)framebuffer_width) {
            x = 0;
            y += 20;
        }
    }
}

void kernel(uint32_t* multiboot_info) {
    if (framebuffer_init(multiboot_info) != 0) {
        while (1) {
            __asm__ volatile ("hlt");
        }
    }

    draw_desktop();

    PUTSTRING(
        "VORTEX OS I",
        10,
        20,
        BLACK
    );

    while (1) {
        __asm__ volatile ("hlt");
    }
}