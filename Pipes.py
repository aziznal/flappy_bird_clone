from typing import List

import pygame

from Pipe import Pipe


class Pipes:

    def __init__(self, *pipe_offsets: List[int]) -> None:
        """
        pipe_offsets: *unpacked list of offsets for pipes to be created
        """
        
        self.pipes: List[Pipe] = []

        if len(pipe_offsets) > 0:        
            self.create_multiple_pipes(pipe_offsets)


    def create_multiple_pipes(self, offsets: List[int]) -> None:
        """
        Creates a pipe at each passed offset
        """
        for offset in offsets:
            self.create_pipe(offset)

    def create_pipe(self, pipe_offset: int) -> None:
        """
        Create a new pair of pipes at given offset
        """

        top_pipe = Pipe(offset=pipe_offset, side='TOP')
        bottom_pipe = Pipe(offset=pipe_offset, side='BOTTOM', top_pipe=top_pipe)

        self.pipes.append(top_pipe)
        self.pipes.append(bottom_pipe)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws every pipe in the pipes list
        """

        for pipe in self.pipes:
            pipe.draw(screen)

    def update(self) -> None:
        """
        Calls every pipe's update method
        """

        for pipe in self.pipes:
            pipe.update()
