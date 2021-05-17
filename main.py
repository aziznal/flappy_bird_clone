import pygame

game_clock = pygame.time.Clock()

from GameSettings import *


from Events import handle_events, handle_player_start_game

from Player import Player

from Pipe import Pipe



pygame.init()
pygame.font.init()


def get_screen():
    return pygame.display.set_mode((ScreenSettings.width, ScreenSettings.height))



def get_text(text, size, color, position):

    font = pygame.font.SysFont("consolas", size)

    img = font.render(text, True, color)

    return img, lambda screen: screen.blit(img, position)




def wait_for_player_to_start_game(screen, draw_functions):

    while True:
        has_pressed_space = handle_player_start_game()

        if has_pressed_space:
            break
        

        screen.fill(Colors.screen_background)


        for func in draw_functions:
            func(screen)


        pygame.display.flip()

        game_clock.tick(60)


def run_game(draw_functions, update_funcs, player):

    screen = get_screen()


    wait_for_player_to_start_game(screen, draw_functions)


    while True:

        handle_events(on_player_jump=lambda: birb.jump())

        screen.fill(Colors.screen_background)


        for func in update_funcs:
            func()

        for func in draw_functions:
            func(screen)

        pygame.display.flip()

        game_clock.tick(60)
        



if __name__ == '__main__':

    score, score_draw = get_text("Score", 30, Colors.black, (ScreenSettings.width / 2, 20))

    birb = Player()

    top_pipe = Pipe(offset=0)
    bottom_pipe = Pipe(offset=0, side="BOTTOM", other_pipe=top_pipe)

    top_pipe1 = Pipe(offset=500)
    bottom_pipe1 = Pipe(offset=500, side="BOTTOM", other_pipe=top_pipe1)

    top_pipe2 = Pipe(offset=1000)
    bottom_pipe2 = Pipe(offset=1000, side="BOTTOM", other_pipe=top_pipe2)

    run_game(
        [   
            birb.draw,

            top_pipe.draw,
            bottom_pipe.draw,

            top_pipe1.draw,
            bottom_pipe1.draw,

            top_pipe2.draw,
            bottom_pipe2.draw,

            score_draw

        ],

        [   

            birb.update,

            top_pipe.update,
            bottom_pipe.update,

            top_pipe1.update,
            bottom_pipe1.update,

            top_pipe2.update,
            bottom_pipe2.update,


        ],

        birb

        )