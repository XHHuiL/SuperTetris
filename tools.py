#!/usr/bin/env python
__author__ = "liuhui"
import pygame
import colors
from pygame.locals import *


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

    def __init__(self, ty, color, cnt_pos, status, direction, l_boundary, r_boundary):
        self.ty = ty
        self.color = color
        self.x = cnt_pos[0]
        self.y = cnt_pos[1]
        self.status = status
        self.direction = direction
        self.l_boundary = l_boundary
        self.r_boundary = r_boundary
        self.width = 20
        if self.status == TBuilding.SHOWING:
            self.width = 40

    # set the status of this building
    def set_status(self, status):
        self.status = status
        if self.status == TBuilding.SHOWING:
            self.width = 40

    # set the center point's position of this building
    def set_cnt_pos(self, cnt_pos):
        self.x = cnt_pos[0]
        self.y = cnt_pos[1]

    # set y of this building
    def set_y(self, y):
        self.y = y

    # increase y of this building
    def increase_y(self, dy):
        self.y += dy

    # set the direction of this building
    def set_direction(self, direction):
        self.direction = direction

    # rotation by pressing key 'z' and 'c'
    def rotation(self, key):
        # save the old direction
        old_direction = self.direction

        if key == K_z:
            if self.direction == TBuilding.UP:
                self.direction = TBuilding.RIGHT
            elif self.direction == TBuilding.RIGHT:
                self.direction = TBuilding.DOWN
            elif self.direction == TBuilding.DOWN:
                self.direction = TBuilding.LEFT
            else:
                self.direction = TBuilding.UP
        elif key == K_c:
            if self.direction == TBuilding.UP:
                self.direction = TBuilding.LEFT
            elif self.direction == TBuilding.LEFT:
                self.direction = TBuilding.DOWN
            elif self.direction == TBuilding.DOWN:
                self.direction = TBuilding.RIGHT
            else:
                self.direction = TBuilding.UP

        # judge is it out of boundary after rotation
        out_of_right = self.horizontal_move(K_RIGHT, True)
        if out_of_right:
            self.direction = old_direction
        else:
            self.x -= self.width

        out_of_left = self.horizontal_move(K_LEFT, True)
        if out_of_left:
            self.direction = old_direction
        else:
            self.x += self.width

    # horizontal move by pressing 'RIGHT' and 'LEFT'
    # return True/False to show is it out of boundary
    def horizontal_move(self, key, from_rotation=False):
        # get the left side and the right side
        if self.ty == TBuilding.STRIP:
            if self.direction == TBuilding.UP or self.direction == TBuilding.DOWN:
                x_left = self.x - 2 * self.width
                x_right = self.x + 2 * self.width
            else:
                x_left = self.x - self.width / 2
                x_right = self.x + self.width / 2
        elif self.ty == TBuilding.BLOCK:
            x_left = self.x - self.width
            x_right = self.x + self.width
        elif self.ty == TBuilding.SOIL:
            if self.direction == TBuilding.UP or self.direction == TBuilding.DOWN:
                x_left = self.x - 3 * self.width / 2
                x_right = self.x + 3 * self.width / 2
            else:
                x_left = self.x - self.width
                x_right = self.x + self.width
        else:
            if self.direction == TBuilding.UP or self.direction == TBuilding.DOWN:
                x_right = self.x + self.width
                x_left = self.x - self.width
            elif self.direction == TBuilding.RIGHT:
                x_left = self.x - 2 * self.width
                x_right = self.x + self.width
            else:
                x_left = self.x - self.width
                x_right = self.x + 2 * self.width

        # default: not from rotation
        if not from_rotation:
            # right move
            if key == K_RIGHT:
                if x_right < self.r_boundary - self.width / 2:
                    self.x += self.width
                    return False
                else:
                    return True

            # left move
            if key == K_LEFT:
                if x_left > self.l_boundary + self.width / 2:
                    self.x -= self.width
                    return False
                else:
                    return True

        # from rotation
        else:
            # right move
            if key == K_RIGHT:
                if x_right <= self.r_boundary:
                    self.x += self.width
                    return False
                else:
                    return True

            # left move
            if key == K_LEFT:
                if x_left >= self.l_boundary:
                    self.x -= self.width
                    return False
                else:
                    return True

    # vertical move by auto
    def vertical_move(self):
        pass

    # draw this building
    def draw(self, screen):
        # first according the five types of building
        # case 1 STRIP
        if self.ty == TBuilding.STRIP:
            # second according the four directions
            if self.direction == TBuilding.UP or self.direction == TBuilding.DOWN:
                b_rect = pygame.Rect(self.x - 2 * self.width, self.y - self.width / 2,
                                     4 * self.width, self.width)

                b_points = ((self.x - 2 * self.width, self.y - self.width / 2),
                            (self.x + 2 * self.width, self.y - self.width / 2),
                            (self.x + 2 * self.width, self.y + self.width / 2),
                            (self.x - 2 * self.width, self.y + self.width / 2))

                b_cross_points_1 = ((self.x - self.width, self.y - self.width / 2),
                                    (self.x - self.width, self.y + self.width / 2))

                b_cross_points_2 = ((self.x, self.y - self.width / 2),
                                    (self.x, self.y + self.width / 2))

                b_cross_points_3 = ((self.x + self.width, self.y - self.width / 2),
                                    (self.x + self.width, self.y + self.width / 2))

                pygame.draw.rect(screen, self.color, b_rect)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_3)

            else:
                b_rect = pygame.Rect(self.x - self.width / 2, self.y - 2 * self.width,
                                     self.width, 4 * self.width)

                b_points = ((self.x - self.width / 2, self.y - 2 * self.width),
                            (self.x + self.width / 2, self.y - 2 * self.width),
                            (self.x + self.width / 2, self.y + 2 * self.width),
                            (self.x - self.width / 2, self.y + 2 * self.width))

                b_cross_points_1 = ((self.x - self.width / 2, self.y - self.width),
                                    (self.x + self.width / 2, self.y - self.width))

                b_cross_points_2 = ((self.x - self.width / 2, self.y),
                                    (self.x + self.width / 2, self.y))

                b_cross_points_3 = ((self.x - self.width / 2, self.y + self.width),
                                    (self.x + self.width / 2, self.y + self.width))

                pygame.draw.rect(screen, self.color, b_rect)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_3)

        # case 2 BLOCK
        elif self.ty == TBuilding.BLOCK:
            # second according the four directions
            b_rect = pygame.Rect(self.x - self.width, self.y - self.width,
                                 2 * self.width, 2 * self.width)

            b_points = ((self.x - self.width, self.y - self.width),
                        (self.x + self.width, self.y - self.width),
                        (self.x + self.width, self.y + self.width),
                        (self.x - self.width, self.y + self.width))

            b_cross_points_1 = ((self.x, self.y - self.width),
                                (self.x, self.y + self.width))

            b_cross_points_2 = ((self.x - self.width, self.y),
                                (self.x + self.width, self.y))

            pygame.draw.rect(screen, self.color, b_rect)
            pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
            pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
            pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

        # case 3 SOIL
        elif self.ty == TBuilding.SOIL:
            # second according the four directions
            if self.direction == TBuilding.UP:
                b_rect_1 = pygame.Rect(self.x - self.width / 2, self.y - self.width,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - 3 * self.width / 2, self.y,
                                       3 * self.width, self.width)

                b_points_1 = ((self.x - self.width / 2, self.y - self.width),
                              (self.x + self.width / 2, self.y - self.width),
                              (self.x + self.width / 2, self.y),
                              (self.x - self.width / 2, self.y))

                b_points_2 = ((self.x - 3 * self.width / 2, self.y),
                              (self.x + 3 * self.width / 2, self.y),
                              (self.x + 3 * self.width / 2, self.y + self.width),
                              (self.x - 3 * self.width / 2, self.y + self.width))

                b_cross_points_1 = ((self.x - self.width / 2, self.y),
                                    (self.x - self.width / 2, self.y + self.width))

                b_cross_points_2 = ((self.x + self.width / 2, self.y),
                                    (self.x + self.width / 2, self.y + self.width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.RIGHT:
                b_rect_1 = pygame.Rect(self.x, self.y - self.width / 2,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - self.width, self.y - 3 * self.width / 2,
                                       self.width, 3 * self.width)

                b_points_1 = ((self.x, self.y - self.width / 2),
                              (self.x + self.width, self.y - self.width / 2),
                              (self.x + self.width, self.y + self.width / 2),
                              (self.x, self.y + self.width / 2))

                b_points_2 = ((self.x - self.width, self.y - 3 * self.width / 2),
                              (self.x, self.y - 3 * self.width / 2),
                              (self.x, self.y + 3 * self.width / 2),
                              (self.x - self.width, self.y + 3 * self.width / 2))

                b_cross_points_1 = ((self.x - self.width, self.y - self.width / 2),
                                    (self.x, self.y - self.width / 2))

                b_cross_points_2 = ((self.x - self.width, self.y + self.width / 2),
                                    (self.x, self.y + self.width / 2))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.DOWN:
                b_rect_1 = pygame.Rect(self.x - self.width / 2, self.y,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - 3 * self.width / 2, self.y - self.width,
                                       3 * self.width, self.width)

                b_points_1 = ((self.x - self.width / 2, self.y),
                              (self.x + self.width / 2, self.y),
                              (self.x + self.width / 2, self.y + self.width),
                              (self.x - self.width / 2, self.y + self.width))

                b_points_2 = ((self.x - 3 * self.width / 2, self.y - self.width),
                              (self.x + 3 * self.width / 2, self.y - self.width),
                              (self.x + 3 * self.width / 2, self.y),
                              (self.x - 3 * self.width / 2, self.y))

                b_cross_points_1 = ((self.x - self.width / 2, self.y - self.width),
                                    (self.x - self.width / 2, self.y))

                b_cross_points_2 = ((self.x + self.width / 2, self.y - self.width),
                                    (self.x + self.width / 2, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            else:
                b_rect_1 = pygame.Rect(self.x - self.width, self.y - self.width / 2,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x, self.y - 3 * self.width / 2,
                                       self.width, 3 * self.width)

                b_points_1 = ((self.x - self.width, self.y - self.width / 2),
                              (self.x, self.y - self.width / 2),
                              (self.x, self.y + self.width / 2),
                              (self.x - self.width, self.y + self.width / 2))

                b_points_2 = ((self.x, self.y - 3 * self.width / 2),
                              (self.x + self.width, self.y - 3 * self.width / 2),
                              (self.x + self.width, self.y + 3 * self.width / 2),
                              (self.x, self.y + 3 * self.width / 2))

                b_cross_points_1 = ((self.x, self.y - self.width / 2),
                                    (self.x + self.width, self.y - self.width / 2))

                b_cross_points_2 = ((self.x, self.y + self.width / 2),
                                    (self.x + self.width, self.y + self.width / 2))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

        # case 4 RIGHT_SEVEN
        elif self.ty == TBuilding.RIGHT_SEVEN:
            # second according the four directions
            if self.direction == TBuilding.UP:
                b_rect_1 = pygame.Rect(self.x, self.y - self.width,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - self.width, self.y - self.width,
                                       self.width, 3 * self.width)

                b_points_1 = ((self.x, self.y - self.width),
                              (self.x + self.width, self.y - self.width),
                              (self.x + self.width, self.y),
                              (self.x, self.y))

                b_points_2 = ((self.x - self.width, self.y - self.width),
                              (self.x, self.y - self.width),
                              (self.x, self.y + 2 * self.width),
                              (self.x - self.width, self.y + 2 * self.width))

                b_cross_points_1 = ((self.x - self.width, self.y),
                                    (self.x, self.y))

                b_cross_points_2 = ((self.x - self.width, self.y + self.width),
                                    (self.x, self.y + self.width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.RIGHT:
                b_rect_1 = pygame.Rect(self.x, self.y,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - 2 * self.width, self.y - self.width,
                                       3 * self.width, self.width)

                b_points_1 = ((self.x, self.y),
                              (self.x + self.width, self.y),
                              (self.x + self.width, self.y + self.width),
                              (self.x, self.y + self.width))

                b_points_2 = ((self.x - 2 * self.width, self.y - self.width),
                              (self.x + self.width, self.y - self.width),
                              (self.x + self.width, self.y),
                              (self.x - 2 * self.width, self.y))

                b_cross_points_1 = ((self.x - self.width, self.y - self.width),
                                    (self.x - self.width, self.y))

                b_cross_points_2 = ((self.x, self.y - self.width),
                                    (self.x, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.DOWN:
                b_rect_1 = pygame.Rect(self.x - self.width, self.y,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x, self.y - 2 * self.width,
                                       self.width, 3 * self.width)

                b_points_1 = ((self.x - self.width, self.y),
                              (self.x, self.y),
                              (self.x, self.y + self.width),
                              (self.x - self.width, self.y + self.width))

                b_points_2 = ((self.x, self.y - 2 * self.width),
                              (self.x + self.width, self.y - 2 * self.width),
                              (self.x + self.width, self.y + self.width),
                              (self.x, self.y + self.width))

                b_cross_points_1 = ((self.x, self.y - self.width),
                                    (self.x + self.width, self.y - self.width))

                b_cross_points_2 = ((self.x, self.y),
                                    (self.x + self.width, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            else:
                b_rect_1 = pygame.Rect(self.x - self.width, self.y - self.width,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - self.width, self.y,
                                       3 * self.width, self.width)

                b_points_1 = ((self.x - self.width, self.y - self.width),
                              (self.x, self.y - self.width),
                              (self.x, self.y),
                              (self.x - self.width, self.y))

                b_points_2 = ((self.x - self.width, self.y),
                              (self.x + 2 * self.width, self.y),
                              (self.x + 2 * self.width, self.y + self.width),
                              (self.x - self.width, self.y + self.width))

                b_cross_points_1 = ((self.x, self.y),
                                    (self.x, self.y + self.width))

                b_cross_points_2 = ((self.x + self.width, self.y),
                                    (self.x + self.width, self.y + self.width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

        # case 5 LEFT_SEVEN
        else:
            # second according the four directions
            if self.direction == TBuilding.UP:
                b_rect_1 = pygame.Rect(self.x - self.width, self.y - self.width,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x, self.y - self.width,
                                       self.width, 3 * self.width)

                b_points_1 = ((self.x - self.width, self.y - self.width),
                              (self.x, self.y - self.width),
                              (self.x, self.y),
                              (self.x - self.width, self.y))

                b_points_2 = ((self.x, self.y - self.width),
                              (self.x + self.width, self.y - self.width),
                              (self.x + self.width, self.y + 2 * self.width),
                              (self.x, self.y + 2 * self.width))

                b_cross_points_1 = ((self.x, self.y),
                                    (self.x + self.width, self.y))

                b_cross_points_2 = ((self.x, self.y + self.width),
                                    (self.x + self.width, self.y + self.width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.RIGHT:
                b_rect_1 = pygame.Rect(self.x, self.y - self.width,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - 2 * self.width, self.y,
                                       3 * self.width, self.width)

                b_points_1 = ((self.x, self.y - self.width),
                              (self.x + self.width, self.y - self.width),
                              (self.x + self.width, self.y),
                              (self.x, self.y))

                b_points_2 = ((self.x - 2 * self.width, self.y),
                              (self.x + self.width, self.y),
                              (self.x + self.width, self.y + self.width),
                              (self.x - 2 * self.width, self.y + self.width))

                b_cross_points_1 = ((self.x - self.width, self.y),
                                    (self.x - self.width, self.y + self.width))

                b_cross_points_2 = ((self.x, self.y),
                                    (self.x, self.y + self.width))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            elif self.direction == TBuilding.DOWN:
                b_rect_1 = pygame.Rect(self.x, self.y,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - self.width, self.y - 2 * self.width,
                                       self.width, 3 * self.width)

                b_points_1 = ((self.x, self.y),
                              (self.x + self.width, self.y),
                              (self.x + self.width, self.y + self.width),
                              (self.x, self.y + self.width))

                b_points_2 = ((self.x - self.width, self.y - 2 * self.width),
                              (self.x, self.y - 2 * self.width),
                              (self.x, self.y + self.width),
                              (self.x - self.width, self.y + self.width))

                b_cross_points_1 = ((self.x - self.width, self.y - self.width),
                                    (self.x, self.y - self.width))

                b_cross_points_2 = ((self.x - self.width, self.y),
                                    (self.x, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)

            else:
                b_rect_1 = pygame.Rect(self.x - self.width, self.y,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - self.width, self.y - self.width,
                                       3 * self.width, self.width)

                b_points_1 = ((self.x - self.width, self.y),
                              (self.x, self.y),
                              (self.x, self.y + self.width),
                              (self.x - self.width, self.y + self.width))

                b_points_2 = ((self.x - self.width, self.y - self.width),
                              (self.x + 2 * self.width, self.y - self.width),
                              (self.x + 2 * self.width, self.y),
                              (self.x - self.width, self.y))

                b_cross_points_1 = ((self.x, self.y - self.width),
                                    (self.x, self.y))

                b_cross_points_2 = ((self.x + self.width, self.y - self.width),
                                    (self.x + self.width, self.y))

                pygame.draw.rect(screen, self.color, b_rect_1)
                pygame.draw.rect(screen, self.color, b_rect_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
