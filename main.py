from PlayerController import PlayerController
from typing import Callable, List
import pygame

from GameSettings import *

from Events import handle_events, handle_player_start_game, handle_quit
from Player import Player
from Pipes import Pipes
from TextObject import TextObject

pygame.init()
pygame.font.init()

game_clock = pygame.time.Clock()


def get_screen() -> pygame.Surface:
    """
    Returns screen object
    """
    return pygame.display.set_mode((ScreenSettings.width, ScreenSettings.height))


def display_start_screen(
    screen: pygame.Surface,
    draw_functions: List[Callable[[pygame.Surface], None]]
    ) -> None:

    start_text = TextObject(
        text="Press Space to Start",
        font_size=56,
        color=Colors.black,
        position=(ScreenSettings.width/2, ScreenSettings.height/2 - 100)
    )

    while True:

        has_pressed_space = handle_player_start_game()

        if has_pressed_space:
            break
        

        screen.fill(Colors.screen_background)


        for func in draw_functions:
            func(screen)
            start_text.draw(screen)


        pygame.display.flip()

        game_clock.tick(60)


def display_gameover_screen(screen: pygame.Surface) -> None:
    
    gameover_text = TextObject(
        text="Gameover!",
        font_size=56,
        color=Colors.red,
        position=(ScreenSettings.width/2, ScreenSettings.height/2 - 100)
    )

    while True:

        handle_quit(pygame.event.get())

        screen.fill(Colors.screen_background)

        gameover_text.draw(screen)

        pygame.display.flip()

        game_clock.tick(60)


def start_game_loop(
    screen: pygame.Surface,
    draw_functions: List[Callable[[pygame.Surface], None]],
    update_functions: List[Callable[[], None]], 
    player: Player
    ) -> None:
    while True:

        handle_events(on_player_jump=lambda: player.jump())

        screen.fill(Colors.screen_background)

        for func in update_functions:
            func()

        for func in draw_functions:
            func(screen)

        pygame.display.flip()

        game_clock.tick(60)


def run_game(
    screen: pygame.Surface,
    draw_functions: List[Callable[[pygame.Surface], None]],
    update_functions: List[Callable[[], None]],
    player: Player
    ) -> None:

    display_start_screen(screen, draw_functions)

    start_game_loop(screen, draw_functions, update_functions, player)
        

if __name__ == '__main__':

    screen = get_screen()

    score_text = TextObject(
        text="Score: ",
        font_size=30,
        color=Colors.black,
        position=(ScreenSettings.width/2, 20)
    )

    pipes = Pipes(0, 500, 1000)
    
    birb = Player(on_death=lambda: display_gameover_screen(screen), pipes = [])

    # controller =  PlayerController([])
    # controller.make_player_jump_at_a_constant_rate()

    run_game(

        screen=screen,
        player=birb,
        draw_functions=[
            birb.draw,
            pipes.draw,
            score_text.draw,
            # controller.draw
        ],
        update_functions=[   
            birb.update,
            pipes.update,
            # controller.update
        ]

    )