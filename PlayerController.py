from typing import List

from Player import Player
from Pipe import Pipe

import threading

# NOTE: ( ͡° ͜ʖ ͡°) 'Threading' in dangerous territory here.
def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator


class PlayerController:
    def __init__(self, pipes: List[Pipe]):
        
        self.pipes = pipes

        self.player = Player(lambda: print("ded"), self.pipes)

    @setInterval(.367)
    def make_player_jump_at_a_constant_rate(self) -> None:
        self.player.jump()


    def draw(self, screen) -> None:
        self.player.draw(screen)


    def update(self) -> None:
        self.player.update()
