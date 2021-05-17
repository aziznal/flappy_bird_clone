
import pygame


def handle_quit(events):

    for event in events:
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                exit()


def handle_keyboard(events, on_player_jump):

    for event in events:
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                on_player_jump()

            

def handle_player_start_game():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return event.key == pygame.K_SPACE
                


def handle_events(on_player_jump):

    events = pygame.event.get()


    handle_quit(events)

    handle_keyboard(events, on_player_jump)

