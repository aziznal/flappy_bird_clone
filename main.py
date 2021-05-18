import pygame

game_clock = pygame.time.Clock()

from GameSettings import *


from Events import handle_events, handle_player_start_game, handle_quit

from Player import Player

from Pipe import Pipe



pygame.init()
pygame.font.init()


def get_screen():
    return pygame.display.set_mode((ScreenSettings.width, ScreenSettings.height))



def get_text(text, size, color, position):

    font = pygame.font.SysFont("arial", size)

    img = font.render(text, True, color)

    return img, lambda screen: screen.blit(img, position)




def wait_for_player_to_start_game(screen, draw_functions):

    start_text, start_text_draw = get_text("Press Space to Start", size=56, color=Colors.black, position=(ScreenSettings.width/2 - 300, ScreenSettings.height/2 - 200))

    while True:

        has_pressed_space = handle_player_start_game()

        if has_pressed_space:
            break
        

        screen.fill(Colors.screen_background)


        for func in draw_functions:
            func(screen)
            start_text_draw(screen)


        pygame.display.flip()

        game_clock.tick(60)


def on_player_death(screen, draw_functions):
    
    while True:


        handle_quit(pygame.event.get())


        screen.fill(Colors.screen_background)

        for func in draw_functions:
            func(screen)


        pygame.display.flip()

        game_clock.tick(60)


def run_game(screen, draw_functions, update_funcs, player):

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

    screen = get_screen()

    score, score_draw = get_text("Score", 30, Colors.black, (ScreenSettings.width / 2, 20))
    gameover_text, gameover_text_draw = get_text(
        "Game over!",
        size=56,
        color=Colors.red,
        position=(ScreenSettings.width/2 - 100, ScreenSettings.height/2 - 100)
    )

    birb = Player(on_death=lambda: on_player_death(screen, [gameover_text_draw]))

    top_pipe = Pipe(offset=0, player=birb)
    bottom_pipe = Pipe(offset=0, side="BOTTOM", other_pipe=top_pipe, player=birb)

    top_pipe1 = Pipe(offset=500, player=birb)
    bottom_pipe1 = Pipe(offset=500, side="BOTTOM", other_pipe=top_pipe1, player=birb)

    top_pipe2 = Pipe(offset=1000, player=birb)
    bottom_pipe2 = Pipe(offset=1000, side="BOTTOM", other_pipe=top_pipe2, player=birb)

    run_game(

        screen,

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