import numpy as np

ITEM_LENGTH = 0
ITEM_WIDTH = 1
ITEM_HEIGHT = 2
ITEM_QUANTITY = 3
ITEM_ROTATION = 4
ITEM_X = 5
ITEM_Y = 6
ITEM_Z = 7
ITEM_INDEX = 8
ITEM_AXIS_LOCK = 9


# ================BIN====================
BIN_LENGTH = 0
BIN_WIDTH = 1
BIN_HEIGHT = 2
BIN_X = 3
BIN_Y = 4
BIN_Z = 5
BIN_ID = 6

# ==============ROTATION=================

ROTATION = np.array(
    [[0, 1, 2], [1, 0, 2], [0, 2, 1], [1, 2, 0], [2, 1, 0], [2, 0, 1]], np.int_
)

FULL_ROTATION = np.array(range(len(ROTATION)), np.int_)
LOCK_ROTATION = np.array([0, 1], np.int_)

# ===============AXIS==================
LENGTH = 0
WIDTH = 1
HEIGHT = 2
