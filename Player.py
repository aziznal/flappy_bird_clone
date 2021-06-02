from typing import Callable, List, Tuple
import pygame

from GameSettings import *

from Pipe import Pipe


class Player:
    def __init__(self, on_death: Callable[[], None], pipes: List[Pipe]) -> None:
        """
        on_death: callback method for when player dies
        """
        
        self.on_death = on_death
        self.pipes = pipes

        self.color = Colors.blue
        
        self.x, self.y = self.get_spawn_location()

        self.width, self.height = PlayerSettings.width, PlayerSettings.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Jump logic states
        self.started_jumping = False
        self.in_mid_jump = False
        self.total_jumped = 0

        # Falling states and acceleration vars
        self.current_gravity_t = GravitySettings.time_vector[0]
        self.index_of_next_gravity_t = 1


    def get_spawn_location(self) -> Tuple[float, float]:
        return (ScreenSettings.width // 4, ScreenSettings.height // 2)


    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws player
        """

        pygame.draw.rect(screen, self.color, self.rect)

        # outline
        pygame.draw.rect(screen, Colors.black, self.rect, width=1)


    def update(self) -> None:
        """
        Updates player's states, position, and jump status.
        """

        self.check_if_out_of_bounds()

        self.check_collision_with_pipes()

        if self.started_jumping or self.in_mid_jump:
            self.handle_jumping()

        else:
            self.fall()


    def handle_jumping(self) -> None:
        """
        Handles player jumping, and checks if they jumped within another jump or from freefall etc.
        """

        # Triggered new jump
        if self.started_jumping:
            
            # Jumped while in mid-jump
            if self.in_mid_jump:
                self.started_jumping = True
                self.in_mid_jump = False

                # Reset player's current jump amount so they start jumping again from their current height
                self.total_jumped = 0
            
            # Jumped from freefall
            else:
                self.started_jumping = False
                self.in_mid_jump = True

        # Continuing previous jump
        elif self.in_mid_jump:
            self.execute_jump()

    def execute_jump(self) -> None:
        """
        handles inner logic of jumping
        """

        # Jump has finished. snap back to reality. oh there goes gravity.
        if self.total_jumped >= PlayerSettings.jump_height_limit:
            self.total_jumped = 0
            self.started_jumping = False
            self.in_mid_jump = False

        else:
            self.total_jumped += PlayerSettings.jump_increment_per_frame
            self.rect.y -= PlayerSettings.jump_increment_per_frame

    def jump(self) -> None:
        """
        This method is called when the player's jump action is triggered
        """
        self.started_jumping = True
        self.current_gravity_t = GravitySettings.time_vector[0]
        self.index_of_next_gravity_t = 1


    def fall(self) -> None:
        """
        Drop player at an accelerating speed
        """
        # Based on this physics equation: v_1 = v_0*t + 1/2*a*t^2
        self.rect.y += PlayerSettings.fall_speed * self.current_gravity_t + .5*GravitySettings.acceleration*(self.current_gravity_t**2)
        self.current_gravity_t = self.get_next_gravity_t()
    
    def get_next_gravity_t(self) -> int:
        """
        Returns next t which either increases player fall acceleration or keeps
        it at terminal velocity
        """

        if self.index_of_next_gravity_t < len(GravitySettings.time_vector) - 1:
            self.index_of_next_gravity_t += 1
            return GravitySettings.time_vector[self.index_of_next_gravity_t - 1]

        # If at terminal velocity, then t stops changing
        else:
            return GravitySettings.time_vector[-1]


    def check_if_out_of_bounds(self) -> None:
        """
        Check if player y is within screen
        """
        if self.rect.bottom >= ScreenSettings.height\
            or self.rect.top <= 0:
            self.die()

    def check_collision_with_pipes(self) -> None:
                
        for pipe in self.pipes:
            if pygame.Rect.colliderect(self.rect, pipe.body_rect) \
                or pygame.Rect.colliderect(self.rect, pipe.tip_rect):
                self.die()
        

    def die(self) -> None:
        """
        This method is called when this player has satisfied a condition for death
        """
        self.color = Colors.red
        self.on_death()
    