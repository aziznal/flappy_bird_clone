
import pygame
from GameSettings import *


class Player:
    def __init__(self):
        
        self.x, self.y = ScreenSettings.width//4, ScreenSettings.height//2

        self.width, self.height = PlayerSettings.width, PlayerSettings.height


        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.started_jumping = False
        self.in_mid_jump = False
        self.total_jumped = 0

        self.current_time = GravitySettings.time_vector[0]
        self.next_time_index = 1


    def draw(self, screen):

        pygame.draw.rect(screen, Colors.red, self.rect)

        # outline
        pygame.draw.rect(screen, Colors.black, self.rect, width=1)


    def update(self):

        if not self.in_mid_jump and not self.started_jumping:
            self.fall()

        if self.started_jumping:

            if self.in_mid_jump:
                self.started_jumping = True
                self.in_mid_jump = False

                # Reset player's current jump amount so they start jumping again from their current height
                self.total_jumped = 0
            
            else:
                self.started_jumping = False
                self.in_mid_jump = True

        if self.in_mid_jump:
            self.execute_jump()


    def execute_jump(self):


        # Jump has finished. snap back to reality. oh there goes gravity.
        if self.total_jumped >= PlayerSettings.jump_height_limit:
                self.total_jumped = 0
                self.started_jumping = False
                self.in_mid_jump = False

        else:
            self.total_jumped += PlayerSettings.jump_increment_per_frame
            self.rect.y -= PlayerSettings.jump_increment_per_frame


    def jump(self):
        self.started_jumping = True
        self.current_time = GravitySettings.time_vector[0]
        self.next_time_index = 1


    def get_next_time(self):

        if self.next_time_index < len(GravitySettings.time_vector) - 1:
            self.next_time_index += 1
            return GravitySettings.time_vector[self.next_time_index - 1]

        # If at terminal velocity, then t stops changing
        else:
            return GravitySettings.time_vector[-1]


    def fall(self):
        self.rect.y += PlayerSettings.fall_speed * self.current_time + .5*GravitySettings.acceleration*(self.current_time**2)
        self.current_time = self.get_next_time()
