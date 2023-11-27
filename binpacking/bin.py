from dataclasses import dataclass, field

import numpy as np

from . import constant as const


@dataclass
class Bin:
    length: int
    width: int
    height: int
    x: int
    y: int
    z: int
    id: int
    free_boxes: list[np.ndarray] = field(default_factory=list)
    packed_boxes: list[np.ndarray] = field(default_factory=list)
    packed_items: list[np.ndarray] = field(default_factory=list)
    regulations: list[np.ndarray] = field(default_factory=list)

    def __post_init__(self):
        self.free_boxes.append(self.bin_in_numpy)

    @classmethod
    def from_numpy_array(cls, np_bin):
        return cls(
            np_bin[const.BIN_LENGTH],
            np_bin[const.BIN_WIDTH],
            np_bin[const.BIN_HEIGHT],
            np_bin[const.BIN_X],
            np_bin[const.BIN_Y],
            np_bin[const.BIN_Z],
            np_bin[const.BIN_ID],
        )

    @property
    def bin_in_numpy(self):
        return np.array(
            [self.length, self.width, self.height, self.x, self.y, self.z, self.id],
            np.int_,
        )
