import math
import random as rd

import constant as const
import numpy as np
import plotly.graph_objects as go
from numba import njit


@njit(cache=True)
def rotate_to_max_fit(box, item):
    best_number_fit = -1
    best_rotation = -1
    best_fit_in_axis = np.zeros(3, np.int_)

    is_lock_oz = item[const.ITEM_AXIS_LOCK] == 1

    possible_rotation = const.LOCK_ROTATION if is_lock_oz else const.FULL_ROTATION

    for rotation in possible_rotation:
        rotated_item = rotate(item, rotation)

        fit_in_axis = compute_number_of_fit(box, rotated_item)
        number_fit = np.prod(fit_in_axis)

        if number_fit > best_number_fit:
            best_number_fit = number_fit
            best_rotation = rotation
            best_fit_in_axis = fit_in_axis

    return best_fit_in_axis, best_rotation


@njit(cache=True)
def compute_number_of_fit(box, item):
    max_by_length = math.floor(box[const.BIN_LENGTH] / item[const.ITEM_LENGTH])
    max_by_width = math.floor(box[const.BIN_WIDTH] / item[const.ITEM_WIDTH])
    max_by_height = math.floor(box[const.BIN_HEIGHT] / item[const.ITEM_HEIGHT])

    return np.array([max_by_length, max_by_width, max_by_height], np.int_)


@njit(cache=True)
def rotate(item, rotation):
    rotated_item = np.copy(item)
    rotated_item[:3] = item[const.ROTATION[rotation]]
    return rotated_item


@njit(cache=True)
def compute_box(box, item, fit_in_axis, rotation):
    boxes = np.empty((6, len(box)), np.int_)

    for i in range(6):
        boxes[i] = np.copy(box)

    nb_fit = np.prod(fit_in_axis)

    if nb_fit == 0:
        return boxes

    # max_by_length = fit_in_axis[const.LENGTH]
    max_by_width = fit_in_axis[const.WIDTH]
    max_by_height = fit_in_axis[const.HEIGHT]

    rotated_item = rotate(item, rotation)

    item_length = rotated_item[const.ITEM_LENGTH]
    item_width = rotated_item[const.ITEM_WIDTH]
    item_height = rotated_item[const.ITEM_HEIGHT]
    item_qty = rotated_item[const.ITEM_QUANTITY]

    box_length = box[const.BIN_LENGTH]
    box_width = box[const.BIN_WIDTH]
    box_height = box[const.BIN_HEIGHT]
    box_x = box[const.BIN_X]
    box_y = box[const.BIN_Y]
    box_z = box[const.BIN_Z]

    temp_qty = item_qty if item_qty < nb_fit else nb_fit

    # N_l
    nb_slice_in_length = math.ceil(temp_qty / (max_by_width * max_by_height))
    # num_item_front
    nb_front_item = temp_qty - (nb_slice_in_length - 1) * max_by_width * max_by_height
    # OF
    usage_length_axis = nb_slice_in_length * item_length
    # HI
    usage_width_axis = max_by_width * item_width
    # num_colum_face
    nb_front_column = math.ceil(nb_front_item / max_by_height)
    # FA
    column_width = nb_front_column * item_width
    # AB
    # todo: confuse
    underfeed_column_height = (
        max_by_height - (nb_front_column * max_by_height - nb_front_item)
    ) * item_height
    # FC
    full_column_width = math.floor(nb_front_item / max_by_height) * item_width
    # FD
    one_full_column_height = max_by_height * item_height

    boxes[0][0:7] = [
        box_length - usage_length_axis,
        box_width,
        box_height,
        box_x + usage_length_axis,
        box_y,
        box_z,
        0,
    ]
    boxes[1][0:7] = [
        item_length,
        box_width - column_width,
        box_height,
        box_x + usage_length_axis - item_length,
        box_y + column_width,
        box_z,
        1,
    ]
    boxes[2][0:7] = [
        item_length,
        column_width - full_column_width,
        box_height - underfeed_column_height,
        box_x + usage_length_axis - item_length,
        box_y + full_column_width,
        underfeed_column_height + box_z,
        2,
    ]
    boxes[3][0:7] = [
        item_length,
        full_column_width,
        box_height - one_full_column_height,
        box_x + usage_length_axis - item_length,
        box_y,
        one_full_column_height + box_z,
        3,
    ]
    boxes[4][0:7] = [
        usage_length_axis - item_length,
        box_width - usage_width_axis,
        box_height,
        box_x,
        box_y + usage_width_axis,
        box_z,
        5,
    ]
    boxes[5][0:7] = [
        usage_length_axis - item_length,
        usage_width_axis,
        box_height - one_full_column_height,
        box_x,
        box_y,
        box_z + one_full_column_height,
        6,
    ]

    return boxes


@njit(cache=True)
def decompose_box(box, item):
    fit_in_axis, rotation = rotate_to_max_fit(box, item)

    boxes = compute_box(box, item, fit_in_axis, rotation)

    if item[const.ITEM_QUANTITY] == 0:
        boxes = np.zeros((6, len(box)), np.int_)
        boxes[0] = np.copy(box)

    return boxes


def get_random_color():
    return "#%06x" % rd.randint(0, 0xFFFFFF)


def draw_boxes(boxes):
    color_list = []
    for i in range(1000):
        color_list.append(get_random_color())

    data = []

    for box in boxes:
        box_x = box[const.BIN_X]
        box_y = box[const.BIN_Y]
        box_z = box[const.BIN_Z]

        box_extreme_x = box_x + box[const.BIN_LENGTH]
        box_extreme_y = box_y + box[const.BIN_WIDTH]
        box_extreme_z = box_z + box[const.BIN_HEIGHT]

        data.append(
            go.Mesh3d(
                x=[
                    box_x,
                    box_x,
                    box_extreme_x,
                    box_extreme_x,
                    box_x,
                    box_x,
                    box_extreme_x,
                    box_extreme_x,
                ],
                y=[
                    box_y,
                    box_extreme_y,
                    box_extreme_y,
                    box_y,
                    box_y,
                    box_extreme_y,
                    box_extreme_y,
                    box_y,
                ],
                z=[
                    box_z,
                    box_z,
                    box_z,
                    box_z,
                    box_extreme_z,
                    box_extreme_z,
                    box_extreme_z,
                    box_extreme_z,
                ],
                # Intensity of each vertex, which will be interpolated and color-coded
                # i, j and k give the vertices of triangles
                i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                showscale=True,
                color=get_random_color(),
                opacity=1,
                flatshading=True,
            )
        )
        data.append(go.Scatter3d(x=[0], y=[0], z=[0], mode="markers"))

    fig = go.Figure(data)
    fig.update_layout(
        autosize=False,
        width=1300,
        height=900,
        scene_aspectmode="data",
        scene_camera=dict(eye=dict(x=-2, y=-2, z=-1)),
    )

    fig.show()


# b = decompose_box(
#     np.array([10, 10, 10, 0, 0, 0, 0]), np.array([2, 3, 4, 20, 0, 0, 0, 0, 0, 0])
# )
#
# draw_boxes(b)
#
# a = 1
