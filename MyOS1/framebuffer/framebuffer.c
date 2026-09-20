//framebuffer.c
#include <stdint.h>
#include "../declarations.h"

uint32_t* framebuffer = 0;

uint32_t framebuffer_width = 0;
uint32_t framebuffer_height = 0;
uint32_t framebuffer_pitch = 0;
uint8_t framebuffer_bpp = 0;

uint8_t framebuffer_red_position = 0;
uint8_t framebuffer_green_position = 0;
uint8_t framebuffer_blue_position = 0;

uint32_t framebuffer_pack_color(uint32_t rgb) {
    uint32_t r = (rgb >> 16) & 0xFF;
    uint32_t g = (rgb >> 8) & 0xFF;
    uint32_t b = rgb & 0xFF;

    return
        (r << framebuffer_red_position) |
        (g << framebuffer_green_position) |
        (b << framebuffer_blue_position);
}

int framebuffer_init(uint32_t* multiboot_info) {
    if (!multiboot_info) {
        return -1;
    }

    uint32_t total_size = multiboot_info[0];

    uint8_t* tag_address = (uint8_t*)multiboot_info + 8;

    while ((uint32_t)(tag_address - (uint8_t*)multiboot_info) < total_size) {
        uint32_t tag_type = *(uint32_t*)tag_address;
        uint32_t tag_size = *(uint32_t*)(tag_address + 4);

        if (tag_type == 0) {
            break;
        }

        if (tag_type == 8) {
            uint64_t framebuffer_address =
                *(uint64_t*)(tag_address + 8);

            framebuffer_pitch =
                *(uint32_t*)(tag_address + 16);

            framebuffer_width =
                *(uint32_t*)(tag_address + 20);

            framebuffer_height =
                *(uint32_t*)(tag_address + 24);

            framebuffer_bpp =
                *(uint8_t*)(tag_address + 28);

            uint8_t framebuffer_type =
                *(uint8_t*)(tag_address + 29);

            if (framebuffer_type != 1) {
                return -2;
            }

            framebuffer_red_position =
                *(uint8_t*)(tag_address + 32);

            framebuffer_green_position =
                *(uint8_t*)(tag_address + 34);

            framebuffer_blue_position =
                *(uint8_t*)(tag_address + 36);

            if (framebuffer_bpp != 32) {
                return -3;
            }

            framebuffer =
                (uint32_t*)(uintptr_t)framebuffer_address;

            return 0;
        }

        tag_address += (tag_size + 7) & ~7;
    }

    return -4;
}

void put_pixel(int x, int y, uint32_t color) {
    if (!framebuffer) {
        return;
    }

    if (x < 0 || y < 0) {
        return;
    }

    if ((uint32_t)x >= framebuffer_width ||
        (uint32_t)y >= framebuffer_height) {
        return;
    }

    uint32_t* pixels =
        (uint32_t*)((uint8_t*)framebuffer +
        ((uint64_t)y * framebuffer_pitch));

    pixels[x] = framebuffer_pack_color(color);
}

void put_pixelLine(int x, int i, int y, uint32_t color) {
    for (; x <= i; x++) {
        put_pixel(x, y, color);
    }
}

int draw_desktop(void) {
    if (!framebuffer) {
        return -1;
    }

    uint32_t color = framebuffer_pack_color(CYAN);

    for (uint32_t y = 0; y < framebuffer_height; y++) {
        uint32_t* pixels =
            (uint32_t*)((uint8_t*)framebuffer +
            ((uint64_t)y * framebuffer_pitch));

        for (uint32_t x = 0; x < framebuffer_width; x++) {
            pixels[x] = color;
        }
    }

    return 0;
}