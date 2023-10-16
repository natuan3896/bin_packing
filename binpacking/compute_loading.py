import math

import constant as const
import numpy as np


def rotate_to_max_fit(bin, item):
    best_number_fit = -1
    best_rotation = -1
    best_fit_in_axis = np.zeros(3, np.int_)

    is_lock_oz = item[const.ITEM_AXIS_LOCK] == 1

    possible_rotation = const.LOCK_ROTATION if is_lock_oz else const.FULL_ROTATION

    for rotation in possible_rotation:
        rotated_item = rotate(item, rotation)

        fit_in_axis = compute_number_of_fit(bin, rotated_item)
        number_fit = np.prod(fit_in_axis)

        if number_fit > best_number_fit:
            best_number_fit = number_fit
            best_rotation = rotation
            best_fit_in_axis = fit_in_axis

    return best_fit_in_axis, best_rotation


def compute_number_of_fit(bin, item):
    max_by_length = math.floor(bin[const.BIN_LENGTH] / item[const.ITEM_LENGTH])
    max_by_width = math.floor(bin[const.BIN_WIDTH] / item[const.ITEM_WIDTH])
    max_by_height = math.floor(bin[const.BIN_HEIGHT] / item[const.ITEM_HEIGHT])

    max_by_length * max_by_width * max_by_width * max_by_height

    return np.array([max_by_length, max_by_width, max_by_height], np.int_)


def rotate(item, rotation):
    rotated_item = np.copy(item)
    rotated_item[:3] = item[const.ROTATION[rotation]]
    return rotated_item


def compute_box(bin, item, fit_in_axis, rotation):
    np.prod(fit_in_axis)
    fit_in_axis[const.LENGTH]
    fit_in_axis[const.WIDTH]
    fit_in_axis[const.HEIGHT]

    rotated_item = rotate(item, rotation)

    rotated_item[const.ITEM_LENGTH]
    rotated_item[const.ITEM_WIDTH]
    rotated_item[const.ITEM_HEIGHT]
    rotated_item[const.ITEM_QUANTITY]


def decompose_bin(bin, item):
    fit_in_axis, rotation = rotate_to_max_fit(bin, item)

    rotate(item, rotation)


b = rotate_to_max_fit(
    np.array([10, 10, 10, 0, 0, 0, 0]), np.array([1, 2, 3, 1, 0, 0, 0, 0, 0, 0])
)

a = 1
