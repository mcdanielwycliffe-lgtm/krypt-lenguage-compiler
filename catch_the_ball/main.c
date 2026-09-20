//main.c
#define SDL_MAIN_HANDLED
#include <SDL2/SDL.h>
#include <stdbool.h>

#include "font.c"

const char (*get_char(char c))[17] {

    switch(c) {
        case 'A': return A;
        case 'B': return B;
        case 'C': return C;
        case 'D': return D;
        case 'E': return E;
        case 'F': return F;
        case 'G': return G;
        case 'H': return H;
        case 'I': return I;
        case 'J': return J;
        case 'K': return K;
        case 'L': return L;
        case 'M': return M;
        case 'N': return N;
        case 'O': return O;
        case 'P': return P;
        case 'Q': return Q;
        case 'R': return R;
        case 'S': return S;
        case 'T': return T;
        case 'U': return U;
        case 'V': return V;
        case 'W': return W;
        case 'X': return X;
        case 'Y': return Y;
        case 'Z': return Z;
    }

    return NULL;
}

void draw_char(
    SDL_Renderer* renderer,
    const char font[9][17],
    int x,
    int y,
    int scale
) {
    for(int row = 0; row < 9; row++) {

        for(int col = 0; col < 16; col++) {

            if(font[row][col] == '1') {

                SDL_Rect pixel = {
                    x + col * scale,
                    y + row * scale,
                    scale,
                    scale
                };

                SDL_RenderFillRect(renderer, &pixel);
            }
        }
    }
}

void draw_text(
    SDL_Renderer* renderer,
    const char* text,
    int x,
    int y,
    int scale
) {
    while(*text) {

        if(*text == ' ') {
            x += 10 * scale;
        }
        else {

            const char (*font)[17] = get_char(*text);

            if(font) {
                draw_char(
                    renderer,
                    font,
                    x,
                    y,
                    scale
                );

                x += 18 * scale;
            }
        }

        text++;
    }
}

int main() {

    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window* window = SDL_CreateWindow(
        "WINDOW",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        800,
        600,
        SDL_WINDOW_SHOWN
    );

    SDL_Renderer* renderer = SDL_CreateRenderer(
        window,
        -1,
        SDL_RENDERER_ACCELERATED
    );

    SDL_Rect player = {
        0, 300,
        50, 350
    };

    SDL_Rect ball = {
        0, 0,
        50, 50
    };

    bool running = true;
    bool win = false;

    SDL_Event event;

    while(running) {

        while(SDL_PollEvent(&event)) {

            if(event.type == SDL_QUIT) {
                running = false;
            }

            if(event.type == SDL_KEYDOWN && !win) {

                if(event.key.keysym.sym == SDLK_w) {
                    player.y -= 5;
                }

                if(event.key.keysym.sym == SDLK_s) {
                    player.y += 5;
                }

                if(event.key.keysym.sym == SDLK_a) {
                    player.x -= 5;
                }

                if(event.key.keysym.sym == SDLK_d) {
                    player.x += 5;
                }

                if(SDL_HasIntersection(&player, &ball)) {
                    win = true;
                }
            }
        }

        SDL_Delay(16);

        SDL_SetRenderDrawColor(
            renderer,
            255, 255, 255, 255
        );

        SDL_RenderClear(renderer);

        SDL_SetRenderDrawColor(
            renderer,
            135, 206, 235, 255
        );

        SDL_RenderFillRect(
            renderer,
            &player
        );

        SDL_SetRenderDrawColor(
            renderer,
            255, 0, 0, 255
        );

        SDL_RenderFillRect(
            renderer,
            &ball
        );

        if(win) {

            SDL_SetRenderDrawColor(
                renderer,
                0, 255, 0, 255
            );

            draw_text(
                renderer,
                "YOU WIN",
                110,
                270,
                5
            );
        }

        SDL_RenderPresent(renderer);
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}