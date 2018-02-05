#!/usr/bin/env python
__author__ = "liuhui"
import pygame
import colors


class TBuilding:
    # five type
    STRIP = 1
    ############
    #          #
    #          #
    #   ####   #
    #          #
    #          #
    ############

    BLOCK = 2
    ############
    #          #
    #    ##    #
    #    ##    #
    #          #
    #          #
    ############

    SOIL = 3
    ############
    #          #
    #    #     #
    #   ###    #
    #          #
    #          #
    ############

    RIGHT_SEVEN = 4
    ############
    #          #
    #    ##    #
    #    #     #
    #    #     #
    #          #
    ############

    LEFT_SEVEN = 5
    ############
    #          #
    #    ##    #
    #     #    #
    #     #    #
    #          #
    ############

    # three status
    FALLING = 1
    STOPPING = 2
    SHOWING = 3

    # four directions
    # default direction is up
    # use key c to change in this order: UP--RIGHT--DOWN--LEFT
    # use key z to change in this order: UP--LEFT-DOWN-RIGHT
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4

    # the outline's color of these buildings
    OUTLINE_COLOR = colors.White

    def __init__(self, ty, color, cnt_pos, status, direction):
        self.ty = ty
        self.color = color
        self.x = cnt_pos[0]
        self.y = cnt_pos[1]
        self.status = status
        self.direction = direction

    # set the status of this building
    def set_status(self, status):
        self.status = status

    # set the center point's position of this building
    def set_cnt_pos(self, cnt_pos):
        self.x = cnt_pos[0]
        self.y = cnt_pos[1]

    # set the direction of this building
    def set_direction(self, direction):
        self.direction = direction

    # draw this building
    def draw(self, screen):
        # first according showing status set the width of square
        # default width of square is 20
        width = 20
        if self.status == TBuilding.SHOWING:
            width = 40

        # second according the five types of building
        # case 1 STRIP
        if self.ty == TBuilding.STRIP:
            # third according the four directions
            if self.direction == TBuilding.UP or self.direction == TBuilding.DOWN:
                b_rect = pygame.Rect(self.x - 2 * width, self.y - width / 2,
                                     4 * width, width)

                b_points = ((self.x - 2 * width, self.y - width / 2),
                            (self.x + 2 * width, self.y - width / 2),
                            (self.x + 2 * width, self.y + width / 2),
                            (self.x - 2 * width, self.y + width / 2))

                b_cross_points_1 = ((self.x - width, self.y - width / 2),
                                    (self.x - width, self.y + width / 2))

                b_cross_points_2 = ((self.x, self.y - width / 2),
                                    (self.x, self.y + width / 2))

                b_cross_points_3 = ((self.x + width, self.y - width / 2),
                                    (self.x + width, self.y + width / 2))

                pygame.draw.rect(screen, self.color, b_rect)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_3)

            else:
                b_rect = pygame.Rect(self.x - width / 2, self.y - 2 * width,
                                     width, 4 * width)

                b_points = ((self.x - width / 2, self.y - 2 * width),
                            (self.x + width / 2, self.y - 2 * width),
                            (self.x + width / 2, self.y + 2 * width),
                            (self.x - width / 2, self.y + 2 * width))

                b_cross_points_1 = ((self.x - width / 2, self.y - width),
                                    (self.x + width / 2, self.y - width))

                b_cross_points_2 = ((self.x - width / 2, self.y),
                                    (self.x + width / 2, self.y))

                b_cross_points_3 = ((self.x - width / 2, self.y + width),
                                    (self.x + width / 2, self.y + width))

                pygame.draw.rect(screen, self.color, b_rect)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_3)

        # case 2 BLOCK
        elif self.ty == TBuilding.BLOCK:
            # third according the four directions
            b_rect = pygame.Rect(self.x - width, self.y - width,
                                 2 * width, 2 * width)

            b_points = ((self.x - width, self.y - width),
                        (self.x + width, self.y - width),
                        (self.x + width, self.y + width),
                        (self.x - width, self.y + width))

            b_cross_points_1 = ((self.x, self.y - width),
                                (self.x, self.y + width))

            b_cross_points_2 = ((self.x - width, self.y),
                                (self.x + width, self.y))

            pygame.draw.rect(screen, self.color, b_rect)
            pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
            pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
            pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

        # case 3 SOIL
        elif self.ty == TBuilding.SOIL:
            # third according the four directions
            if self.direction == TBuilding.UP:
                b_rect_1 = pygame.Rect(self.x - width / 2, self.y - width,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - 3 * width / 2, self.y,
                                       3 * width, width)

                b_points_1 = ((self.x - width / 2, self.y - width),
                              (self.x + width / 2, self.y - width),
                              (self.x + width / 2, self.y),
                              (self.x - width / 2, self.y))

                b_points_2 = ((self.x - 3 * width / 2, self.y),
                              (self.x + 3 * width / 2, self.y),
                              (self.x + 3 * width / 2, self.y + width),
                              (self.x - 3 * width / 2, self.y + width))

                b_cross_points_1 = ((self.x - width / 2, self.y),
                                    (self.x - width / 2, self.y + width))

                b_cross_points_2 = ((self.x + width / 2, self.y),
                                    (self.x + width / 2, self.y + width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.RIGHT:
                b_rect_1 = pygame.Rect(self.x, self.y - width / 2,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - width, self.y - 3 * width / 2,
                                       width, 3 * width)

                b_points_1 = ((self.x, self.y - width / 2),
                              (self.x + width, self.y - width / 2),
                              (self.x + width, self.y + width / 2),
                              (self.x, self.y + width / 2))

                b_points_2 = ((self.x - width, self.y - 3 * width / 2),
                              (self.x, self.y - 3 * width / 2),
                              (self.x, self.y + 3 * width / 2),
                              (self.x - width, self.y + 3 * width / 2))

                b_cross_points_1 = ((self.x - width, self.y - width / 2),
                                    (self.x, self.y - width / 2))

                b_cross_points_2 = ((self.x - width, self.y + width / 2),
                                    (self.x, self.y + width / 2))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.DOWN:
                b_rect_1 = pygame.Rect(self.x - width / 2, self.y,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - 3 * width / 2, self.y - width,
                                       3 * width, width)

                b_points_1 = ((self.x - width / 2, self.y),
                              (self.x + width / 2, self.y),
                              (self.x + width / 2, self.y + width),
                              (self.x - width / 2, self.y + width))

                b_points_2 = ((self.x - 3 * width / 2, self.y - width),
                              (self.x + 3 * width / 2, self.y - width),
                              (self.x + 3 * width / 2, self.y),
                              (self.x - 3 * width / 2, self.y))

                b_cross_points_1 = ((self.x - width / 2, self.y - width),
                                    (self.x - width / 2, self.y))

                b_cross_points_2 = ((self.x + width / 2, self.y - width),
                                    (self.x + width / 2, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            else:
                b_rect_1 = pygame.Rect(self.x - width, self.y - width / 2,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x, self.y - 3 * width / 2,
                                       width, 3 * width)

                b_points_1 = ((self.x - width, self.y - width / 2),
                              (self.x, self.y - width / 2),
                              (self.x, self.y + width / 2),
                              (self.x - width, self.y + width / 2))

                b_points_2 = ((self.x, self.y - 3 * width / 2),
                              (self.x + width, self.y - 3 * width / 2),
                              (self.x + width, self.y + 3 * width / 2),
                              (self.x, self.y + 3 * width / 2))

                b_cross_points_1 = ((self.x, self.y - width / 2),
                                    (self.x + width, self.y - width / 2))

                b_cross_points_2 = ((self.x, self.y + width / 2),
                                    (self.x + width, self.y + width / 2))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

        # case 4 RIGHT_SEVEN
        elif self.ty == TBuilding.RIGHT_SEVEN:
            # third according the four directions
            if self.direction == TBuilding.UP:
                b_rect_1 = pygame.Rect(self.x, self.y - width,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - width, self.y - width,
                                       width, 3 * width)

                b_points_1 = ((self.x, self.y - width),
                              (self.x + width, self.y - width),
                              (self.x + width, self.y),
                              (self.x, self.y))

                b_points_2 = ((self.x - width, self.y - width),
                              (self.x, self.y - width),
                              (self.x, self.y + 2 * width),
                              (self.x - width, self.y + 2 * width))

                b_cross_points_1 = ((self.x - width, self.y),
                                    (self.x, self.y))

                b_cross_points_2 = ((self.x - width, self.y + width),
                                    (self.x, self.y + width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.RIGHT:
                b_rect_1 = pygame.Rect(self.x, self.y,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - 2 * width, self.y - width,
                                       3 * width, width)

                b_points_1 = ((self.x, self.y),
                              (self.x + width, self.y),
                              (self.x + width, self.y + width),
                              (self.x, self.y + width))

                b_points_2 = ((self.x - 2 * width, self.y - width),
                              (self.x + width, self.y - width),
                              (self.x + width, self.y),
                              (self.x - 2 * width, self.y))

                b_cross_points_1 = ((self.x - width, self.y - width),
                                    (self.x - width, self.y))

                b_cross_points_2 = ((self.x, self.y - width),
                                    (self.x, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.DOWN:
                b_rect_1 = pygame.Rect(self.x - width, self.y,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x, self.y - 2 * width,
                                       width, 3 * width)

                b_points_1 = ((self.x - width, self.y),
                              (self.x, self.y),
                              (self.x, self.y + width),
                              (self.x - width, self.y + width))

                b_points_2 = ((self.x, self.y - 2 * width),
                              (self.x + width, self.y - 2 * width),
                              (self.x + width, self.y + width),
                              (self.x, self.y + width))

                b_cross_points_1 = ((self.x, self.y - width),
                                    (self.x + width, self.y - width))

                b_cross_points_2 = ((self.x, self.y),
                                    (self.x + width, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            else:
                b_rect_1 = pygame.Rect(self.x - width, self.y - width,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - width, self.y,
                                       3 * width, width)

                b_points_1 = ((self.x - width, self.y - width),
                              (self.x, self.y - width),
                              (self.x, self.y),
                              (self.x - width, self.y))

                b_points_2 = ((self.x - width, self.y),
                              (self.x + 2 * width, self.y),
                              (self.x + 2 * width, self.y + width),
                              (self.x - width, self.y + width))

                b_cross_points_1 = ((self.x, self.y),
                                    (self.x, self.y + width))

                b_cross_points_2 = ((self.x + width, self.y),
                                    (self.x + width, self.y + width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

        # case 5 LEFT_SEVEN
        else:
            # third according the four directions
            if self.direction == TBuilding.UP:
                b_rect_1 = pygame.Rect(self.x - width, self.y - width,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x, self.y - width,
                                       width, 3 * width)

                b_points_1 = ((self.x - width, self.y - width),
                              (self.x, self.y - width),
                              (self.x, self.y),
                              (self.x - width, self.y))

                b_points_2 = ((self.x, self.y - width),
                              (self.x + width, self.y - width),
                              (self.x + width, self.y + 2 * width),
                              (self.x, self.y + 2 * width))

                b_cross_points_1 = ((self.x, self.y),
                                    (self.x + width, self.y))

                b_cross_points_2 = ((self.x, self.y + width),
                                    (self.x + width, self.y + width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.RIGHT:
                b_rect_1 = pygame.Rect(self.x, self.y - width,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - 2 * width, self.y,
                                       3 * width, width)

                b_points_1 = ((self.x, self.y - width),
                              (self.x + width, self.y - width),
                              (self.x + width, self.y),
                              (self.x, self.y))

                b_points_2 = ((self.x - 2 * width, self.y),
                              (self.x + width, self.y),
                              (self.x + width, self.y + width),
                              (self.x - 2 * width, self.y + width))

                b_cross_points_1 = ((self.x - width, self.y),
                                    (self.x - width, self.y + width))

                b_cross_points_2 = ((self.x, self.y),
                                    (self.x, self.y + width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.DOWN:
                b_rect_1 = pygame.Rect(self.x, self.y,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - width, self.y - 2 * width,
                                       width, 3 * width)

                b_points_1 = ((self.x, self.y),
                              (self.x + width, self.y),
                              (self.x + width, self.y + width),
                              (self.x, self.y + width))

                b_points_2 = ((self.x - width, self.y - 2 * width),
                              (self.x, self.y - 2 * width),
                              (self.x, self.y + width),
                              (self.x - width, self.y + width))

                b_cross_points_1 = ((self.x - width, self.y - width),
                                    (self.x, self.y - width))

                b_cross_points_2 = ((self.x - width, self.y),
                                    (self.x, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            else:
                b_rect_1 = pygame.Rect(self.x - width, self.y,
                                       width, width)

                b_rect_2 = pygame.Rect(self.x - width, self.y - width,
                                       3 * width, width)

                b_points_1 = ((self.x - width, self.y),
                              (self.x, self.y),
                              (self.x, self.y + width),
                              (self.x - width, self.y + width))

                b_points_2 = ((self.x - width, self.y - width),
                              (self.x + 2 * width, self.y - width),
                              (self.x + 2 * width, self.y),
                              (self.x - width, self.y))

                b_cross_points_1 = ((self.x, self.y - width),
                                    (self.x, self.y))

                b_cross_points_2 = ((self.x + width, self.y - width),
                                    (self.x + width, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
