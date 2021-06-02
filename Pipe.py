import pygame

from typing import Literal, Union

from GameSettings import *


class Pipe:

    def __init__(self, offset: int =0, side: Literal['TOP', 'BOTTOM']='TOP', top_pipe=None) -> None:
        """
        offset: x offset to spawn the pipe at. this also affects where the pipe 'rolls back' around the screen

        side: "TOP" or "BOTTOM". specifies which side of the screen the pipe is on.

        top_pipe: Reference to TOP pipe. Set only if this is bottom pipe.

        player: reference to player to check collisions
        """

        self.check_side_and_top_pipe_reference(side, top_pipe)

        self.side = side
        self.offset = offset
        self.top_pipe = top_pipe
        
        # Pipe Size and Location Settings
        self.width = PipeSettings.width
        self.height = self.set_height()

        # X starts out of bounds on right of screen plus a little buffer
        self.starting_x = ScreenSettings.width + self.width + 100 + self.offset

        self.body_rect = self.get_body_rect()
        self.tip_rect = self.get_tip_rect()


    def check_side_and_top_pipe_reference(self, side, top_pipe_reference) -> None:
        if side not in ["TOP", "BOTTOM"]:
            raise ValueError(f'"side" argument must be either "TOP" or "BOTTOM". Got {side} instead')

        if side == "TOP" and top_pipe_reference is not None:
            raise ValueError("Cannot assign reference to top pipe if this is not a bottom pipe")

    def set_height(self) -> Union[int, float]:
        """
        Returns a pipe height in accordance with game rules.
        i.e if Top pipe, then returned height is random, and if Bottom pipe,
        then returned height is calculated to leave a certain distance from top pipe
        and then extend to bottom of screen
        """
        if self.side == "BOTTOM":
            return self.get_height_according_to_other_pipe()

        else:
            return PipeSettings.get_random_height()

    def get_height_according_to_other_pipe(self) -> Union[int, float]:
        """
        Leave a distance of player_jump_height * 2.5 to keep the game fair.
        """

        height = ScreenSettings.height - self.top_pipe.height - (PlayerSettings.jump_height_limit*2.5)

        return height


    def get_body_rect(self) -> pygame.Rect:
        """
        Returns a pygame.Rect object for pipe body
        """
        
        self.x = self.starting_x

        # Y changes depending on whether this is top or bottom side pipe
        self.y = self.determine_y_from_side()

        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_tip_rect(self) -> pygame.Rect:
        """
        Returns a pygame.Rect object for pipe tip
        """

        return pygame.Rect(
            
            self.body_rect.centerx - PipeSettings.tip_width // 2,
            
            self.determine_tip_y_from_side(),
            
            PipeSettings.tip_width,
            
            PipeSettings.tip_height
        )


    def determine_y_from_side(self) -> int:
        """
        Return pipe y according to its side
        """
        if self.side == "TOP":
            # Top pipe always starts at y = 0
            y = 0

        elif self.side == "BOTTOM":
            # Bottom pipe is offsetted from max y according to its height
            y = ScreenSettings.height - self.height

        else:
            self.check_side_and_top_pipe_reference(self.side, self.top_pipe)

        return y

    def determine_tip_y_from_side(self) -> int:
        """
        Return pipe tip's y according to pipe side
        """

        tip_y = 0

        if self.side == "TOP":
            # Raise up if on top side
            tip_y = self.height - PipeSettings.tip_height

        elif self.side == "BOTTOM":
            # Push down if on bottom
            tip_y = self.y - PipeSettings.tip_height + 1

        else:
            self.check_side_and_top_pipe_reference(self.side, self.top_pipe)

        return tip_y


    def draw(self, screen) -> None:
        """
        Draws pipe body and tip to screen
        """

        # A Pipe is two shapes: the wide bit at the tip and the slightly narrower body
        self.draw_body(screen)
        self.draw_tip(screen)

    def draw_body(self, screen) -> None:
        """
        Draw pipe body
        """
        pygame.draw.rect(screen, Colors.green, self.body_rect)

        # outline
        pygame.draw.rect(screen, Colors.black, self.body_rect, width=1)

    def draw_tip(self, screen) -> None:
        """
        Draws pipe tip
        """
        pygame.draw.rect(screen, Colors.green, self.tip_rect)

        # outline
        pygame.draw.rect(screen, Colors.black, self.tip_rect, width=1)


    def update(self) -> None:
        """
        Update states and check collisions
        """
        
        self.move_left()
        self.check_if_past_screen_left()


    def move_left(self) -> None:
        """
        Moves pipe and tip to left every frame by pre-determined amount
        """
        self.body_rect.x -= PipeSettings.scroll_left_speed
        self.tip_rect.x -= PipeSettings.scroll_left_speed

    def check_if_past_screen_left(self) -> None:
        """
        if pipe is past left bounds, this method moves it to screen right and gives it a new height
        """

        # Body
        if self.body_rect.right < 0:
            self.body_rect.left = self.starting_x - self.offset - 100
            self.tip_rect.centerx = self.body_rect.centerx

            # Make it seem like a new pipe popped out after this one is out of bounds
            self.set_new_random_height()

    def set_new_random_height(self) -> None:
        """
        Assign new random height to pipe
        """
        
        self.height = self.set_height()        

        # Y changes depending on whether this is top or bottom side pipe
        self.y = self.determine_y_from_side()

        self.body_rect.height = self.height
        self.body_rect.y = self.y

        self.tip_rect = self.get_tip_rect()
