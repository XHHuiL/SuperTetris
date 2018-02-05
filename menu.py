#!/usr/bin/env python
__author__ = "liuhui"
import colors
import pygame
import random
from tools import TBuilding
from pygame.locals import *

# define some constant
PLAY_OPTION_TEXT = "play"
LEVEL_OPTION_TEXT = "level"
HELP_OPTION_TEXT = "help"

PLAY_OPTION_Y = 183
LEVEL_OPTION_Y = 230
HELP_OPTION_Y = 277
OPTION_HEIGHT = 38

SCREEN_WIDTH = 520
SCREEN_HEIGHT = 440

LOGO_Y = 86
LOGO_WIDTH = 312
LOGO_HEIGHT = 54

# define the control variables
# three variables used to switch interface
PLAY_OPTION_CHOSEN = False
LEVEL_OPTION_CHOSEN = False
HELP_OPTION_CHOSEN = False

# four variables used to indicate current interface
IN_MENU = True
IN_PLAY = False
IN_LEVEL = False
IN_HELP = False

# define the level options of level-interface
CURRENT_LEVEL = 1
LEVEL_TEXT_1 = "level 1"
LEVEL_TEXT_2 = "level 2"
LEVEL_TEXT_3 = "level 3"

LEVEL_1_Y = 160
LEVEL_2_Y = 200
LEVEL_3_Y = 240
LEVEL_HEIGHT = 40

LEVEL_1_CHOSEN = False
LEVEL_2_CHOSEN = False
LEVEL_3_CHOSEN = False

# define the tips of help-interface
TIP_1 = "1.press the key 'q' to exit"
TIP_2 = "2.press the key 'p' to pause or unpause bgm"
TIP_3 = "3.press the key 's' to stop or play bgm"
TIP_4 = "4.use mouse to start game, choose level or get help"
TIP_5 = "5.press the key 'ESC' to return to menu-interface"

TIP_HEIGHT = 30
TIP_1_Y = 145
TIP_2_Y = 175
TIP_3_Y = 205
TIP_4_Y = 235
TIP_5_Y = 265

# tow variables used to control bgm
IS_PAUSED = False
IS_STOPPED = False

# variables used in play-interface
READY_PLAY_MES = "please press key 'a' to start game"

IS_PLAYING = False
IS_GAME_PAUSED = False

# three main blocks' position in play-interface
BLOCK_OUTLINE_COLOR = colors.Brown

PLAY_BLOCK_POINTS = ((20, 20), (220, 20), (220, 400), (20, 400))
INF_BLOCK_POINTS = ((240, 20), (500, 20), (500, 400), (240, 400))

# the next building label text and score label text
NEXT_BUILDING_TEXT = "Next:"
SCORE_TEXT = "Score:"
SCORE_NUMBER_TEXT = "000"

LABEL_HEIGHT = 30
NEXT_LABEL_X = 258
NEXT_LABEL_Y = 50
SCORE_LABEL_X = 258
SCORE_LABEL_Y = 240
SCORE_NUMBER_X = 303
SCORE_NUMBER_Y = 280

# next building's x and y
NEXT_BUILDING_X = 380
NEXT_BUILDING_Y = 160
NEXT_BUILDING_POS = (NEXT_BUILDING_X, NEXT_BUILDING_Y)

COLORS = (colors.Red, colors.ChestnutRed, colors.DullRed,
          colors.BrownRed, colors.FireRed, colors.DeepRed,
          colors.Pink, colors.DeepPink, colors.BrightPink,
          colors.LightPink, colors.Purple, colors.DullPurple,
          colors.BluePurple, colors.DeepPurple, colors.MediumPurple,
          colors.LightPurple, colors.Brown, colors.DullBrown,
          colors.RawWoodColor, colors.WheatColor, colors.Peach,
          colors.Yellow, colors.Gold, colors.Khaki,
          colors.LightYellow, colors.Green, colors.BlackishGreen,
          colors.LeekGreen, colors.SeaGreen, colors.LightSeaGreen,
          colors.YellowGreen, colors.GrayGreen, colors.SpringGreen,
          colors.Blue, colors.DullBlue, colors.MediumBlue,
          colors.SkyBlue, colors.Cyan, colors.LightCyan,
          colors.Gray, colors.DarkGray, colors.SlateGray,
          colors.DullGray, colors.SilveryGray, colors.LightGray)

COLORS_MAX_INDEX = 44

TYPES = (TBuilding.STRIP, TBuilding.BLOCK, TBuilding.SOIL,
         TBuilding.RIGHT_SEVEN, TBuilding.LEFT_SEVEN)

TYPES_MAX_INDEX = 4

DIRECTIONS = (TBuilding.UP, TBuilding.RIGHT, TBuilding.DOWN, TBuilding.LEFT)

DIRECTIONS_MAX_INDEX = 3

STATUS = (TBuilding.FALLING, TBuilding.STOPPING, TBuilding.SHOWING)

NEXT_BUILDING = None

SCORE_NUMBER = 0


def main():
    # reference the global variables
    global IN_MENU
    global IN_PLAY
    global IN_LEVEL
    global IN_HELP

    global PLAY_OPTION_CHOSEN
    global LEVEL_OPTION_CHOSEN
    global HELP_OPTION_CHOSEN

    global CURRENT_LEVEL
    global LEVEL_1_CHOSEN
    global LEVEL_2_CHOSEN
    global LEVEL_3_CHOSEN

    global IS_PAUSED
    global IS_STOPPED
    global IS_PLAYING

    global NEXT_BUILDING

    # init
    pygame.init()
    pygame.display.set_caption("Super Tetris")
    screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screen_size, 0, 32)

    ##################################
    ## 1.settings of menu-interface ##
    ##################################

    # create the logo of tetris and set it's position
    tetris_logo = pygame.image.load("data/image/tetris_logo.png").convert_alpha()
    tetris_logo_rect = tetris_logo.get_rect()
    tetris_logo_rect.center = (SCREEN_WIDTH / 2, LOGO_Y + LOGO_HEIGHT / 2)

    # create six font surfaces used in menu interface and set their positions
    normal_size_font = pygame.font.Font("data/font/tetris_cp_mario.ttf", 32)
    focus_size_font = pygame.font.Font("data/font/tetris_cp_mario.ttf", 36)
    play_normal_bt = normal_size_font.render(PLAY_OPTION_TEXT, True, colors.Black)
    play_focus_bt = focus_size_font.render(PLAY_OPTION_TEXT, True, colors.White)
    level_normal_bt = normal_size_font.render(LEVEL_OPTION_TEXT, True, colors.Black)
    level_focus_bt = focus_size_font.render(LEVEL_OPTION_TEXT, True, colors.White)
    help_normal_bt = normal_size_font.render(HELP_OPTION_TEXT, True, colors.Black)
    help_focus_bt = focus_size_font.render(HELP_OPTION_TEXT, True, colors.White)

    play_option_rect = play_normal_bt.get_rect()
    play_option_rect.center = (SCREEN_WIDTH / 2, PLAY_OPTION_Y + OPTION_HEIGHT / 2)
    level_option_rect = level_normal_bt.get_rect()
    level_option_rect.center = (SCREEN_WIDTH / 2, LEVEL_OPTION_Y + OPTION_HEIGHT / 2)
    help_option_rect = help_normal_bt.get_rect()
    help_option_rect.center = (SCREEN_WIDTH / 2, HELP_OPTION_Y + OPTION_HEIGHT / 2)

    # create the background image of menu-interface
    menu_background = pygame.image.load("data/image/menu_background.jpeg").convert()

    # create the background image of help-interface
    help_background = pygame.image.load("data/image/help_background.jpeg").convert()

    # init the mixer of pygame and set max number of channels
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.set_num_channels(8)

    # play the back ground music bgm1
    menu_bgm = pygame.mixer.Sound("data/sound/bgm1.ogg")
    menu_bgm_channel = menu_bgm.play(-1)

    # bgm2
    play_bgm = pygame.mixer.Sound("data/sound/bgm2.ogg")
    play_bgm_channel = None

    # the music used to play when skimming over one of the three options
    skim_over_music = pygame.mixer.Sound("data/sound/skim_over.wav")

    ##################################
    ## 2.settings of play-interface ##
    ##################################

    # prompt to start game
    small_font = pygame.font.Font("data/font/tetris_cp_mario.ttf", 24)
    start_game_prompt = small_font.render(READY_PLAY_MES, True, colors.White)
    start_game_prompt_rect = start_game_prompt.get_rect()
    start_game_prompt_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # the music used to play when ready to play game
    ready_go_music = pygame.mixer.Sound("data/sound/ready_go.wav")

    # three labels
    next_label = small_font.render(NEXT_BUILDING_TEXT, True, colors.White)
    score_label = small_font.render(SCORE_TEXT, True, colors.White)
    score_number_label = small_font.render(SCORE_NUMBER_TEXT, True, colors.White)

    ###################################
    ## 3.settings of level-interface ##
    ###################################

    # the level buttons
    level_1_normal_bt = normal_size_font.render(LEVEL_TEXT_1, True, colors.Black)
    level_1_focus_bt = focus_size_font.render(LEVEL_TEXT_1, True, colors.White)
    level_2_normal_bt = normal_size_font.render(LEVEL_TEXT_2, True, colors.Black)
    level_2_focus_bt = focus_size_font.render(LEVEL_TEXT_2, True, colors.White)
    level_3_normal_bt = normal_size_font.render(LEVEL_TEXT_3, True, colors.Black)
    level_3_focus_bt = focus_size_font.render(LEVEL_TEXT_3, True, colors.White)

    # set level buttons' positions
    level_1_option_rect = level_1_normal_bt.get_rect()
    level_1_option_rect.center = (SCREEN_WIDTH / 2, LEVEL_1_Y + LEVEL_HEIGHT / 2)
    level_2_option_rect = level_2_normal_bt.get_rect()
    level_2_option_rect.center = (SCREEN_WIDTH / 2, LEVEL_2_Y + LEVEL_HEIGHT / 2)
    level_3_option_rect = level_3_normal_bt.get_rect()
    level_3_option_rect.center = (SCREEN_WIDTH / 2, LEVEL_3_Y + LEVEL_HEIGHT / 2)

    ##################################
    ## 4.settings of help-interface ##
    ##################################

    # create four font surface used in help-interface
    v_small_font = pygame.font.Font("data/font/tetris_cp_mario.ttf", 18)
    tip_1 = v_small_font.render(TIP_1, True, colors.White)
    tip_2 = v_small_font.render(TIP_2, True, colors.White)
    tip_3 = v_small_font.render(TIP_3, True, colors.White)
    tip_4 = v_small_font.render(TIP_4, True, colors.White)
    tip_5 = v_small_font.render(TIP_5, True, colors.White)

    # set the positions of these tips
    tip_rect_1 = tip_1.get_rect()
    tip_rect_1.center = (SCREEN_WIDTH / 2, TIP_1_Y + TIP_HEIGHT / 2)
    tip_rect_2 = tip_2.get_rect()
    tip_rect_2.center = (SCREEN_WIDTH / 2, TIP_2_Y + TIP_HEIGHT / 2)
    tip_rect_3 = tip_3.get_rect()
    tip_rect_3.center = (SCREEN_WIDTH / 2, TIP_3_Y + TIP_HEIGHT / 2)
    tip_rect_4 = tip_4.get_rect()
    tip_rect_4.center = (SCREEN_WIDTH / 2, TIP_4_Y + TIP_HEIGHT / 2)
    tip_rect_5 = tip_5.get_rect()
    tip_rect_5.center = (SCREEN_WIDTH / 2, TIP_5_Y + TIP_HEIGHT / 2)

    # main loop
    while True:
        event = pygame.event.wait()

        # listen to the quit event
        if event.type == QUIT:
            quit(0)

        # listen to the key pressed event
        if event.type == KEYDOWN:

            # pause the back ground music
            if event.key == K_p:
                if not IS_STOPPED:
                    if IN_MENU or IN_LEVEL or IN_HELP:
                        if IS_PAUSED:
                            menu_bgm_channel.unpause()
                        else:
                            menu_bgm_channel.pause()
                    else:
                        if IS_PAUSED:
                            play_bgm_channel.unpause()
                        else:
                            play_bgm_channel.pause()
                    IS_PAUSED = not IS_PAUSED

            # stop the back ground music
            if event.key == K_s:
                if IN_MENU or IN_LEVEL or IN_HELP:
                    if IS_STOPPED:
                        menu_bgm_channel = menu_bgm.play(-1)
                    else:
                        menu_bgm.stop()
                else:
                    if IS_STOPPED:
                        play_bgm_channel = play_bgm.play(-1)
                    else:
                        play_bgm.stop()
                IS_STOPPED = not IS_STOPPED

            # turn to menu-interface
            if event.key == K_ESCAPE and not IN_MENU:
                if IN_PLAY:
                    IS_PLAYING = False
                    play_bgm.stop()
                    menu_bgm_channel = menu_bgm.play(-1)
                turn_to_menu()

            # exit
            if event.key == K_q:
                quit(0)

            if event.key == K_a and IN_PLAY and not IS_PLAYING:
                ready_go_music.play()
                IS_PLAYING = True

        # listen to the mouse pressed event in level-interface
        # this statue must be dealt before the next one
        if IN_LEVEL and event.type == MOUSEBUTTONDOWN:
            if LEVEL_1_CHOSEN:
                CURRENT_LEVEL = 1
                turn_to_menu()
            elif LEVEL_2_CHOSEN:
                CURRENT_LEVEL = 2
                turn_to_menu()
            elif LEVEL_3_CHOSEN:
                CURRENT_LEVEL = 3
                turn_to_menu()

        # listen to the mouse pressed event in menu-interface
        if IN_MENU and event.type == MOUSEBUTTONDOWN:
            # switch to the play-interface
            if PLAY_OPTION_CHOSEN:
                IN_MENU = False
                IN_PLAY = True
                PLAY_OPTION_CHOSEN = False
                IS_PAUSED = False
                IS_STOPPED = False
                menu_bgm.stop()
                play_bgm_channel = play_bgm.play(-1)
                NEXT_BUILDING = TBuilding(TYPES[random.randint(0, TYPES_MAX_INDEX)],
                                          COLORS[random.randint(0, COLORS_MAX_INDEX)],
                                          NEXT_BUILDING_POS, TBuilding.SHOWING,
                                          DIRECTIONS[random.randint(0, DIRECTIONS_MAX_INDEX)])
                pass
            # switch to the level-interface
            if LEVEL_OPTION_CHOSEN:
                IN_MENU = False
                IN_LEVEL = True
                CURRENT_LEVEL = 1
                LEVEL_1_CHOSEN = False
                LEVEL_2_CHOSEN = False
                LEVEL_3_CHOSEN = False
                LEVEL_OPTION_CHOSEN = False
                pass
            # switch to the help-interface
            if HELP_OPTION_CHOSEN:
                IN_MENU = False
                IN_HELP = True
                HELP_OPTION_CHOSEN = False
                pass

        # set the background image
        # this step of render must execute first
        if IN_MENU or IN_LEVEL:
            screen.blit(menu_background, (0, 0))
        elif IN_HELP or IN_PLAY:
            screen.blit(help_background, (0, 0))

        # render the three option buttons
        if IN_MENU or IN_LEVEL:
            # listen to the mouse move event
            mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()

            if IN_MENU:
                # set the play option button
                if play_option_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    if not PLAY_OPTION_CHOSEN:
                        PLAY_OPTION_CHOSEN = True
                        skim_over_music.play()
                    screen.blit(play_focus_bt, play_option_rect)
                else:
                    PLAY_OPTION_CHOSEN = False
                    screen.blit(play_normal_bt, play_option_rect)

                # set the level option button
                if level_option_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    if not LEVEL_OPTION_CHOSEN:
                        LEVEL_OPTION_CHOSEN = True
                        skim_over_music.play()
                    screen.blit(level_focus_bt, level_option_rect)
                else:
                    LEVEL_OPTION_CHOSEN = False
                    screen.blit(level_normal_bt, level_option_rect)

                # set the help option button
                if help_option_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    if not HELP_OPTION_CHOSEN:
                        HELP_OPTION_CHOSEN = True
                        skim_over_music.play()
                    screen.blit(help_focus_bt, help_option_rect)
                else:
                    HELP_OPTION_CHOSEN = False
                    screen.blit(help_normal_bt, help_option_rect)
            else:
                # set the level 1 option button
                if level_1_option_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    if not LEVEL_1_CHOSEN:
                        LEVEL_1_CHOSEN = True
                        skim_over_music.play()
                    screen.blit(level_1_focus_bt, level_1_option_rect)
                else:
                    LEVEL_1_CHOSEN = False
                    screen.blit(level_1_normal_bt, level_1_option_rect)
                # set the level 2 option button
                if level_2_option_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    if not LEVEL_2_CHOSEN:
                        LEVEL_2_CHOSEN = True
                        skim_over_music.play()
                    screen.blit(level_2_focus_bt, level_2_option_rect)
                else:
                    LEVEL_2_CHOSEN = False
                    screen.blit(level_2_normal_bt, level_2_option_rect)
                # set the level 3 option button
                if level_3_option_rect.collidepoint(mouse_pos_x, mouse_pos_y):
                    if not LEVEL_3_CHOSEN:
                        LEVEL_3_CHOSEN = True
                        skim_over_music.play()
                    screen.blit(level_3_focus_bt, level_3_option_rect)
                else:
                    LEVEL_3_CHOSEN = False
                    screen.blit(level_3_normal_bt, level_3_option_rect)

        # render the five tips
        if IN_HELP:
            screen.blit(tip_1, tip_rect_1)
            screen.blit(tip_2, tip_rect_2)
            screen.blit(tip_3, tip_rect_3)
            screen.blit(tip_4, tip_rect_4)
            screen.blit(tip_5, tip_rect_5)

        # set the logo
        if IN_MENU:
            screen.blit(tetris_logo, tetris_logo_rect)

        # set the three block in play-interface
        if IN_PLAY and IS_PLAYING:
            pygame.draw.lines(screen, BLOCK_OUTLINE_COLOR, True, PLAY_BLOCK_POINTS)
            pygame.draw.lines(screen, BLOCK_OUTLINE_COLOR, True, INF_BLOCK_POINTS)
            screen.blit(next_label, (NEXT_LABEL_X, NEXT_LABEL_Y))
            screen.blit(score_label, (SCORE_LABEL_X, SCORE_LABEL_Y))
            screen.blit(score_number_label, (SCORE_NUMBER_X, SCORE_NUMBER_Y))
            NEXT_BUILDING.draw(screen)

        # set the prompt message
        if IN_PLAY and not IS_PLAYING:
            screen.blit(start_game_prompt, start_game_prompt_rect)

        # update
        pygame.display.update()


# function used to set some variables when turn to menu-interface
def turn_to_menu():
    global IN_MENU
    global IN_PLAY
    global IN_LEVEL
    global IN_HELP

    global IS_PAUSED
    global IS_STOPPED

    if IN_PLAY:
        IS_PAUSED = False
        IS_STOPPED = False

    IN_MENU = True
    IN_PLAY = False
    IN_LEVEL = False
    IN_HELP = False


if __name__ == "__main__":
    main()
