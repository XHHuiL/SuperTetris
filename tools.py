#!/usr/bin/env python
__author__ = "liuhui"
import pygame
import colors
import math
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

    # width of square
    SQUARE_WIDTH = 20

    # the destroy music
    pygame.init()
    DESTROY_MUSIC = pygame.mixer.Sound("data/sound/destroy.wav")

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
        else:
            self.width = 20

    # set the center point's position of this building
    def set_cnt_pos(self, cnt_pos):
        self.x = cnt_pos[0]
        self.y = cnt_pos[1]

    # set y of this building
    def set_y(self, y):
        self.y = y

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
            elif self.direction == TBuilding.RIGHT:
                x_left = self.x - self.width
                x_right = self.x
            else:
                x_left = self.x
                x_right = self.x + self.width
        elif self.ty == TBuilding.BLOCK:
            x_left = self.x - self.width
            x_right = self.x + self.width
        elif self.ty == TBuilding.SOIL:
            if self.direction == TBuilding.UP:
                x_left = self.x - self.width
                x_right = self.x + 2 * self.width
            elif self.direction == TBuilding.DOWN:
                x_left = self.x - 2 * self.width
                x_right = self.x + self.width
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

    # vertical move by dy
    def vertical_move(self, dy, column_up_boundaries, squares):
        self.y += dy
        square_index_pairs = self.get_square_indexes()

        # four square index pairs
        square_index_pair_1 = square_index_pairs[0]
        square_index_pair_2 = square_index_pairs[1]
        square_index_pair_3 = square_index_pairs[2]
        square_index_pair_4 = square_index_pairs[3]

        # judge
        if square_index_pair_4[0] >= 19:
            self.status = TBuilding.STOPPING

        elif square_index_pair_4[0] >= 0 and squares[square_index_pair_4[0]][square_index_pair_4[1]].is_filled:
            self.status = TBuilding.STOPPING

        if square_index_pair_3[0] >= 19:
            self.status = TBuilding.STOPPING

        elif square_index_pair_3[0] >= 0 and squares[square_index_pair_3[0]][square_index_pair_3[1]].is_filled:
            self.status = TBuilding.STOPPING

        if square_index_pair_2[0] >= 19:
            self.status = TBuilding.STOPPING

        elif square_index_pair_2[0] >= 0 and squares[square_index_pair_2[0]][square_index_pair_2[1]].is_filled:
            self.status = TBuilding.STOPPING

        if square_index_pair_1[0] >= 19:
            self.status = TBuilding.STOPPING

        elif square_index_pair_1[0] >= 0 and squares[square_index_pair_1[0]][square_index_pair_1[1]].is_filled:
            self.status = TBuilding.STOPPING

        # if this building is stopping then update the up boundaries
        if self.status == TBuilding.STOPPING:
            # set the new up boundary
            if square_index_pair_1[0] <= column_up_boundaries[square_index_pair_1[1]] + 1:
                column_up_boundaries[square_index_pair_1[1]] = square_index_pair_1[0] - 2

            if square_index_pair_2[0] <= column_up_boundaries[square_index_pair_2[1]] + 1:
                column_up_boundaries[square_index_pair_2[1]] = square_index_pair_2[0] - 2

            if square_index_pair_3[0] <= column_up_boundaries[square_index_pair_3[1]] + 1:
                column_up_boundaries[square_index_pair_3[1]] = square_index_pair_3[0] - 2

            if square_index_pair_4[0] <= column_up_boundaries[square_index_pair_4[1]] + 1:
                column_up_boundaries[square_index_pair_4[1]] = square_index_pair_4[0] - 2

            # set square filled
            if square_index_pair_1[0] >= 1:
                squares[square_index_pair_1[0] - 1][square_index_pair_1[1]].set_filled(True)
                squares[square_index_pair_1[0] - 1][square_index_pair_1[1]].set_color(self.color)

            if square_index_pair_2[0] >= 1:
                squares[square_index_pair_2[0] - 1][square_index_pair_2[1]].set_filled(True)
                squares[square_index_pair_2[0] - 1][square_index_pair_2[1]].set_color(self.color)

            if square_index_pair_3[0] >= 1:
                squares[square_index_pair_3[0] - 1][square_index_pair_3[1]].set_filled(True)
                squares[square_index_pair_3[0] - 1][square_index_pair_3[1]].set_color(self.color)

            if square_index_pair_4[0] >= 1:
                squares[square_index_pair_4[0] - 1][square_index_pair_4[1]].set_filled(True)
                squares[square_index_pair_4[0] - 1][square_index_pair_4[1]].set_color(self.color)

        # judge whether is stopping
        if self.status == TBuilding.STOPPING:
            is_stopping = True
        else:
            is_stopping = False

        all_filled_row_indexes = []

        # get all the filled row
        if is_stopping:
            for i in range(0, 19):
                count = 0
                for j in range(0, 10):
                    if not squares[18 - i][j].is_filled:
                        break
                    else:
                        count += 1
                if count == 10:
                    all_filled_row_indexes.append(18-i)

        length = len(all_filled_row_indexes)
        # remove all the filled rows
        for i in range(0, length):
            current_index = all_filled_row_indexes[i]
            for j in range(0, current_index - 1):
                for k in range(0, 10):
                    squares[current_index - j][k].is_filled = squares[current_index - j-1][k].is_filled
                    squares[current_index - j][k].color = squares[current_index - j-1][k].color
            for k in range(0, 10):
                squares[0][k].is_filled = False

            # update the following row index
            for j in range(i, length):
                all_filled_row_indexes[j] += 1

        score = 0
        if length == 1:
            score = 100
        elif length == 2:
            score = 2 * 200
        elif length == 3:
            score = 3 * 300
        elif length >= 4:
            score = 4 * 400

        # play the destroy music
        if score > 0:
            TBuilding.DESTROY_MUSIC.play()

        # judge whether is game over
        is_game_over = False
        if is_stopping:
            for i in column_up_boundaries:
                if i < 0:
                    is_game_over = True
                    break

        return is_stopping, is_game_over, score

    # get four square indexes from four left down points
    @staticmethod
    def square_indexes_from_ld_points(points):
        ld_point_1 = points[0]
        ld_point_2 = points[1]
        ld_point_3 = points[2]
        ld_point_4 = points[3]

        # get the square index pair of this building
        # [i, j]
        square_index_pair_1 = [0, 0]
        square_index_pair_2 = [0, 0]
        square_index_pair_3 = [0, 0]
        square_index_pair_4 = [0, 0]

        square_index_pair_1[1] = int(ld_point_1[0]) // TBuilding.SQUARE_WIDTH
        square_index_pair_2[1] = int(ld_point_2[0]) // TBuilding.SQUARE_WIDTH
        square_index_pair_3[1] = int(ld_point_3[0]) // TBuilding.SQUARE_WIDTH
        square_index_pair_4[1] = int(ld_point_4[0]) // TBuilding.SQUARE_WIDTH

        if ld_point_1[1] < 0:
            square_index_pair_1[0] = -1
        else:
            square_index_pair_1[0] = int(ld_point_1[1]) // TBuilding.SQUARE_WIDTH

        if ld_point_2[1] < 0:
            square_index_pair_2[0] = -1
        else:
            square_index_pair_2[0] = int(ld_point_2[1]) // TBuilding.SQUARE_WIDTH

        if ld_point_3[1] < 0:
            square_index_pair_3[0] = -1
        else:
            square_index_pair_3[0] = int(ld_point_3[1]) // TBuilding.SQUARE_WIDTH

        if ld_point_4[1] < 0:
            square_index_pair_4[0] = -1
        else:
            square_index_pair_4[0] = int(ld_point_4[1]) // TBuilding.SQUARE_WIDTH

        # return four square index pairs
        return square_index_pair_1, square_index_pair_2, square_index_pair_3, square_index_pair_4

    # get square indexes according to type and direction of this building
    def get_square_indexes(self):
        if self.ty == TBuilding.STRIP:
            if self.direction == TBuilding.UP:
                # get the left down points of this building
                ld_point_1 = (self.x - 2 * self.width, self.y + self.width)
                ld_point_2 = (self.x - self.width, self.y + self.width)
                ld_point_3 = (self.x, self.y + self.width)
                ld_point_4 = (self.x + self.width, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            elif self.direction == TBuilding.RIGHT:
                # get the left down points of this building
                ld_point_1 = (self.x - self.width, self.y - self.width)
                ld_point_2 = (self.x - self.width, self.y)
                ld_point_3 = (self.x - self.width, self.y + self.width)
                ld_point_4 = (self.x - self.width, self.y + 2 * self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            elif self.direction == TBuilding.DOWN:
                # get the left down points of this building
                ld_point_1 = (self.x - 2 * self.width, self.y)
                ld_point_2 = (self.x - self.width, self.y)
                ld_point_3 = (self.x, self.y)
                ld_point_4 = (self.x + self.width, self.y)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            else:
                # get the left down points of this building
                ld_point_1 = (self.x, self.y - self.width)
                ld_point_2 = (self.x, self.y)
                ld_point_3 = (self.x, self.y + self.width)
                ld_point_4 = (self.x, self.y + 2 * self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

        elif self.ty == TBuilding.BLOCK:
            # get the left down points of this building
            ld_point_1 = (self.x - self.width, self.y)
            ld_point_2 = (self.x, self.y)
            ld_point_3 = (self.x - self.width, self.y + self.width)
            ld_point_4 = (self.x, self.y + self.width)

            points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
            return self.square_indexes_from_ld_points(points)

        elif self.ty == TBuilding.SOIL:
            if self.direction == TBuilding.UP:
                # get the left down points of this building
                ld_point_1 = (self.x, self.y)
                ld_point_2 = (self.x - self.width, self.y + self.width)
                ld_point_3 = (self.x, self.y + self.width)
                ld_point_4 = (self.x + self.width, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            elif self.direction == TBuilding.RIGHT:
                # get the left down points of this building
                ld_point_1 = (self.x - self.width, self.y)
                ld_point_2 = (self.x - self.width, self.y + self.width)
                ld_point_3 = (self.x, self.y + self.width)
                ld_point_4 = (self.x - self.width, self.y + 2 * self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            elif self.direction == TBuilding.DOWN:
                # get the left down points of this building
                ld_point_1 = (self.x - 2 * self.width, self.y)
                ld_point_2 = (self.x - self.width, self.y)
                ld_point_3 = (self.x, self.y)
                ld_point_4 = (self.x - self.width, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            else:
                # get the left down points of this building
                ld_point_1 = (self.x, self.y - self.width)
                ld_point_2 = (self.x - self.width, self.y)
                ld_point_3 = (self.x, self.y)
                ld_point_4 = (self.x, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

        elif self.ty == TBuilding.RIGHT_SEVEN:
            if self.direction == TBuilding.UP:
                # get the left down points of this building
                ld_point_1 = (self.x - self.width, self.y)
                ld_point_2 = (self.x, self.y)
                ld_point_3 = (self.x - self.width, self.y + self.width)
                ld_point_4 = (self.x - self.width, self.y + 2 * self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            elif self.direction == TBuilding.RIGHT:
                # get the left down points of this building
                ld_point_1 = (self.x - 2 * self.width, self.y)
                ld_point_2 = (self.x - self.width, self.y)
                ld_point_3 = (self.x, self.y)
                ld_point_4 = (self.x, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            elif self.direction == TBuilding.DOWN:
                # get the left down points of this building
                ld_point_1 = (self.x, self.y - self.width)
                ld_point_2 = (self.x, self.y)
                ld_point_3 = (self.x - self.width, self.y + self.width)
                ld_point_4 = (self.x, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            else:
                # get the left down points of this building
                ld_point_1 = (self.x - self.width, self.y)
                ld_point_2 = (self.x - self.width, self.y + self.width)
                ld_point_3 = (self.x, self.y + self.width)
                ld_point_4 = (self.x + self.width, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

        else:
            if self.direction == TBuilding.UP:
                # get the left down points of this building
                ld_point_1 = (self.x - self.width, self.y)
                ld_point_2 = (self.x, self.y)
                ld_point_3 = (self.x, self.y + self.width)
                ld_point_4 = (self.x, self.y + 2 * self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            elif self.direction == TBuilding.RIGHT:
                # get the left down points of this building
                ld_point_1 = (self.x, self.y)
                ld_point_2 = (self.x - 2 * self.width, self.y + self.width)
                ld_point_3 = (self.x - self.width, self.y + self.width)
                ld_point_4 = (self.x, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            elif self.direction == TBuilding.DOWN:
                # get the left down points of this building
                ld_point_1 = (self.x - self.width, self.y - self.width)
                ld_point_2 = (self.x - self.width, self.y)
                ld_point_3 = (self.x - self.width, self.y + self.width)
                ld_point_4 = (self.x, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

            else:
                # get the left down points of this building
                ld_point_1 = (self.x - self.width, self.y)
                ld_point_2 = (self.x, self.y)
                ld_point_3 = (self.x + self.width, self.y)
                ld_point_4 = (self.x - self.width, self.y + self.width)

                points = [ld_point_1, ld_point_2, ld_point_3, ld_point_4]
                return self.square_indexes_from_ld_points(points)

    # draw this building
    def draw(self, screen):
        # first according the five types of building
        # case 1 STRIP
        if self.ty == TBuilding.STRIP:
            # second according the four directions
            if self.direction == TBuilding.UP:
                b_rect = pygame.Rect(self.x - 2 * self.width, self.y,
                                     4 * self.width, self.width)

                b_points = ((self.x - 2 * self.width, self.y),
                            (self.x + 2 * self.width, self.y),
                            (self.x + 2 * self.width, self.y + self.width),
                            (self.x - 2 * self.width, self.y + self.width))

                b_cross_points_1 = ((self.x - self.width, self.y),
                                    (self.x - self.width, self.y + self.width))

                b_cross_points_2 = ((self.x, self.y),
                                    (self.x, self.y + self.width))

                b_cross_points_3 = ((self.x + self.width, self.y),
                                    (self.x + self.width, self.y + self.width))

                pygame.draw.rect(screen, self.color, b_rect)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_3)

            elif self.direction == TBuilding.DOWN:
                b_rect = pygame.Rect(self.x - 2 * self.width, self.y - self.width,
                                     4 * self.width, self.width)

                b_points = ((self.x - 2 * self.width, self.y - self.width),
                            (self.x + 2 * self.width, self.y - self.width),
                            (self.x + 2 * self.width, self.y),
                            (self.x - 2 * self.width, self.y))

                b_cross_points_1 = ((self.x - self.width, self.y),
                                    (self.x - self.width, self.y - self.width))

                b_cross_points_2 = ((self.x, self.y),
                                    (self.x, self.y - self.width))

                b_cross_points_3 = ((self.x + self.width, self.y),
                                    (self.x + self.width, self.y - self.width))

                pygame.draw.rect(screen, self.color, b_rect)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_3)

            elif self.direction == TBuilding.RIGHT:
                b_rect = pygame.Rect(self.x - self.width, self.y - 2 * self.width,
                                     self.width, 4 * self.width)

                b_points = ((self.x - self.width, self.y - 2 * self.width),
                            (self.x, self.y - 2 * self.width),
                            (self.x, self.y + 2 * self.width),
                            (self.x - self.width, self.y + 2 * self.width))

                b_cross_points_1 = ((self.x - self.width, self.y - self.width),
                                    (self.x, self.y - self.width))

                b_cross_points_2 = ((self.x - self.width, self.y),
                                    (self.x, self.y))

                b_cross_points_3 = ((self.x - self.width, self.y + self.width),
                                    (self.x, self.y + self.width))

                pygame.draw.rect(screen, self.color, b_rect)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, b_points)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_1)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_2)
                pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, False, b_cross_points_3)

            else:
                b_rect = pygame.Rect(self.x, self.y - 2 * self.width,
                                     self.width, 4 * self.width)

                b_points = ((self.x, self.y - 2 * self.width),
                            (self.x + self.width, self.y - 2 * self.width),
                            (self.x + self.width, self.y + 2 * self.width),
                            (self.x, self.y + 2 * self.width))

                b_cross_points_1 = ((self.x + self.width, self.y - self.width),
                                    (self.x, self.y - self.width))

                b_cross_points_2 = ((self.x + self.width, self.y),
                                    (self.x, self.y))

                b_cross_points_3 = ((self.x + self.width, self.y + self.width),
                                    (self.x, self.y + self.width))

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
                b_rect_1 = pygame.Rect(self.x, self.y - self.width,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - self.width, self.y,
                                       3 * self.width, self.width)

                b_points_1 = ((self.x, self.y - self.width),
                              (self.x + self.width, self.y - self.width),
                              (self.x + self.width, self.y),
                              (self.x, self.y))

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

            elif self.direction == TBuilding.RIGHT:
                b_rect_1 = pygame.Rect(self.x, self.y,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - self.width, self.y - self.width,
                                       self.width, 3 * self.width)

                b_points_1 = ((self.x, self.y),
                              (self.x + self.width, self.y),
                              (self.x + self.width, self.y + self.width),
                              (self.x, self.y + self.width))

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

            elif self.direction == TBuilding.DOWN:
                b_rect_1 = pygame.Rect(self.x - self.width, self.y,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x - 2 * self.width, self.y - self.width,
                                       3 * self.width, self.width)

                b_points_1 = ((self.x - self.width, self.y),
                              (self.x, self.y),
                              (self.x, self.y + self.width),
                              (self.x - self.width, self.y + self.width))

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

            else:
                b_rect_1 = pygame.Rect(self.x - self.width, self.y - self.width,
                                       self.width, self.width)

                b_rect_2 = pygame.Rect(self.x, self.y - 2 * self.width,
                                       self.width, 3 * self.width)

                b_points_1 = ((self.x - self.width, self.y - self.width),
                              (self.x, self.y - self.width),
                              (self.x, self.y),
                              (self.x - self.width, self.y))

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


class TSquare:

    # the construct of TSquare
    def __init__(self, is_filled, x, y, width):
        self.is_filled = is_filled
        self.x = x
        self.y = y
        self.width = width
        self.color = colors.White

    # set filled
    def set_filled(self, is_filled):
        self.is_filled = is_filled

    # set color
    def set_color(self, color):
        self.color = color

    # draw this square in a screen
    def draw(self, screen):
        if self.is_filled:
            s_rect = pygame.Rect(self.x, self.y, self.width, self.width)
            s_points = ((self.x, self.y), (self.x + self.width, self.y),
                        (self.x + self.width, self.y + self.width), (self.x, self.y + self.width))

            pygame.draw.rect(screen, self.color, s_rect)
            pygame.draw.lines(screen, TBuilding.OUTLINE_COLOR, True, s_points)
