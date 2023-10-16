from dataclasses import dataclass

import constant as const
import numpy as np


@dataclass
class Bin:
    length: int
    width: int
    height: int
    x: int
    y: int
    z: int
    id: int

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
