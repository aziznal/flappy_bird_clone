from typing import List, Tuple

from Pipe import Pipe


class Pipes:

    def __init__(self, *args, **kwargs):
        
        self.pipes: List[Pipe] = []


    def create_pipe(self, pipe_offset: int):
        top_pipe = Pipe(pipe_offset, side='BOTTOM')
        bottom_pipe = Pipe(pipe_offset, side='BOTTOM', top_pipe=top_pipe)

        self.pipes.append(top_pipe)
        self.pipes.append(bottom_pipe)


    def draw(self) -> None:
        pass

    def update(self) -> None:
        pass
