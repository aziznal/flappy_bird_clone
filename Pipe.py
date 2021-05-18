import pygame
from random import randint

from GameSettings import *


class Pipe:

    def __init__(self, offset=0, side="TOP", other_pipe=None, player=None):
        
        self.player = player

        if side not in ["TOP", "BOTTOM"]:
            raise ValueError(f'"side" argument must be either "TOP" or "BOTTOM". Got {side} instead')

        self.side = side
        self.offset = offset

        # Bottom pipe will keep a ref to top pipe to help with calculating new height
        self.other_pipe = other_pipe

        self.width = PipeSettings.width
        
        self.height = self.set_height()


        # X starts out of bounds on right of screen plus a little buffer
        self.starting_x = ScreenSettings.width + self.width + 100 + self.offset

        self.body_rect = self.get_body_rect()
        self.tip_rect = self.get_tip_rect()



    def set_height(self):
        if self.side == "BOTTOM":
            return self.get_height_according_to_other_pipe()

        else:
            return PipeSettings.get_random_height()


    def get_height_according_to_other_pipe(self):

        # Bottom side must leave at least jump limit distance from top pipe
        # lower_limit = ScreenSettings.height - self.other_pipe.height - PlayerSettings.jump_height_limit*3
        # upper_limit = ScreenSettings.height - self.other_pipe.height - (PlayerSettings.jump_height_limit*2)

        # height = randint(lower_limit, upper_limit)

        height = upper_limit = ScreenSettings.height - self.other_pipe.height - (PlayerSettings.jump_height_limit*2.5)

        return height


    def get_body_rect(self):
        
        self.x = self.starting_x

        # Y changes depending on whether this is top or bottom side pipe
        self.y = self.determine_y_from_side()

        return pygame.Rect(self.x, self.y, self.width, self.height)


    def get_tip_rect(self):
        return pygame.Rect(
            
            self.body_rect.centerx - PipeSettings.tip_width // 2,
            
            self.determine_tip_y_from_side(),
            
            PipeSettings.tip_width,
            
            PipeSettings.tip_height
        )



    def determine_y_from_side(self):
        if self.side == "TOP":
            # simply start at 0
            y = 0

        else:

            # offset from max screen y by pipe height
            y = ScreenSettings.height - self.height


        return y


    def determine_tip_y_from_side(self):

        if self.side == "TOP":
            # Raise up if on top side
            return self.height - PipeSettings.tip_height

        else:
            # Push down if on bottom
            return self.y - PipeSettings.tip_height + 1



    def draw(self, screen):

        # A Pipe is two shapes: the wide bit at the tip and the slightly narrower body
        self.draw_body(screen)
        self.draw_tip(screen)


    def draw_body(self, screen):
        pygame.draw.rect(screen, Colors.green, self.body_rect)

        # outline
        pygame.draw.rect(screen, Colors.black, self.body_rect, width=1)


    def draw_tip(self, screen):
        pygame.draw.rect(screen, Colors.green, self.tip_rect)

        # outline
        pygame.draw.rect(screen, Colors.black, self.tip_rect, width=1)



    
    def update(self):
        
        self.move_left()
        self.check_out_of_bounds()

        self.check_collision_with_player()



    def move_left(self):
        self.body_rect.x -= PipeSettings.move_speed
        self.tip_rect.x -= PipeSettings.move_speed


    def check_out_of_bounds(self):

        # Body
        if self.body_rect.right < 0:
            self.body_rect.left = self.starting_x - self.offset - 100
            self.tip_rect.centerx = self.body_rect.centerx

            # Make it seem like a new pipe popped out after this one is out of bounds
            self.make_new_height()


    def make_new_height(self):
        
        self.height = self.set_height()        

        # Y changes depending on whether this is top or bottom side pipe
        self.y = self.determine_y_from_side()

        self.body_rect.height = self.height
        self.body_rect.y = self.y

        self.tip_rect = self.get_tip_rect()


    def check_collision_with_player(self):
        if pygame.Rect.colliderect(self.body_rect, self.player.rect) == 1:
            self.player.die()

