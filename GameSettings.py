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
    fall_speed = 8

    jump_height_limit = 120


class PipeSettings:

    width = 150
    height = ScreenSettings.height // 3

    tip_width =  width + 20
    tip_height = 75

    move_speed = 8  # px per frame


    @staticmethod
    def get_random_height():

        return randint(PlayerSettings.jump_height_limit + 10, ScreenSettings.height // 2)