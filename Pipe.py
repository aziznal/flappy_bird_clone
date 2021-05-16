import pygame

from GameSettings import *


class Pipe:

    def __init__(self, offset=0, side="TOP"):
        
        if side not in ["TOP", "BOTTOM"]:
            raise ValueError(f'"side" argument must be either "TOP" or "BOTTOM". Got {side} instead')

        self.side = side
        self.offset = offset
        
        self.width = PipeSettings.width
        self.height = PipeSettings.get_random_height()

        # X starts out of bounds on right of screen plus a little buffer
        self.starting_x = ScreenSettings.width + self.width + 100 + self.offset
        self.x = self.starting_x

        # Y changes depending on whether this is top or bottom side pipe
        self.y = self.determine_y_from_side()

        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.tip_rect = pygame.Rect(self.rect.centerx - PipeSettings.tip_width // 2, self.determine_tip_y_from_side(), PipeSettings.tip_width, PipeSettings.tip_height)


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
        pygame.draw.rect(screen, Colors.green, self.rect)

        # outline
        pygame.draw.rect(screen, Colors.black, self.rect, width=1)


    def draw_tip(self, screen):
        pygame.draw.rect(screen, Colors.green, self.tip_rect)

        # outline
        pygame.draw.rect(screen, Colors.black, self.tip_rect, width=1)



    
    def update(self):
        
        self.move_left()
        self.check_out_of_bounds()



    def move_left(self):
        self.rect.x -= PipeSettings.move_speed
        self.tip_rect.x -= PipeSettings.move_speed


    def check_out_of_bounds(self):

        # Body
        if self.rect.right < 0:
            self.rect.left = self.starting_x - self.offset - 100
            self.tip_rect.centerx = self.rect.centerx

            # Make it seem like a new pipe popped out after this one is out of bounds
            self.make_new_height()


    def make_new_height(self):
        
        self.height = PipeSettings.get_random_height()

        # Y changes depending on whether this is top or bottom side pipe
        self.y = self.determine_y_from_side()

        
        self.rect.height = self.height
        self.rect.y = self.y

        self.tip_rect = pygame.Rect(self.rect.centerx - PipeSettings.tip_width // 2, self.determine_tip_y_from_side(), PipeSettings.tip_width, PipeSettings.tip_height)

