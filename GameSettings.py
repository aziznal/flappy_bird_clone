from random import randint


class Colors:

    white = (255, 255, 255)
    black = (0, 0, 0)

    red, green, blue = (255, 30, 60), (44, 255, 111), (10, 137, 255)

    screen_background = (201, 230, 255)




class ScreenSettings:

    width = 1200
    height = 800



class PlayerSettings:

    width = 50
    height = 50

    # px per frame (multiply by 60)
    fall_speed = 0.4

    jump_height_limit = 90 + 9 *3
    jump_increment_per_frame = 9


class PipeSettings:

    width = 150
    height = ScreenSettings.height // 3

    tip_width =  width + 20
    tip_height = 75

    move_speed = 4  # px per frame


    @staticmethod
    def get_random_height():

        # Height must be at least 20% of the screen height
        # Height will be upto half the screen minus player jump height so game is never technically impossible

        bottom_limit =  ScreenSettings.height * 20/100
        top_limit = ScreenSettings.height * 60/100

        return randint(bottom_limit, top_limit)


class GravitySettings:

    time_vector = list(range(2, 10))   # terminal velocity is reached at t = 59 (one second)

    acceleration = .2    # px / second (probably?)

