from dataclasses import dataclass, field

import constant as const
import numpy as np
import plotly.graph_objects as go
import compute_loading as cl


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

    def draw_bin(self):
        data = []

        data.append(
            go.Mesh3d(
                x=[0, 0, self.length, self.length, 0, 0, self.length,self.length],
                y=[0, self.width, self.width, 0, 0, self.width, self.width,0],
                z=[0, 0, 0, 0, self.height, self.height, self.height,self.height],
                # Intensity of each vertex, which will be interpolated and color-coded
                # i, j and k give the vertices of triangles

                # i  =  [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                # j  =  [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                # k  =  [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                name='y',
                showscale=True,
                color="#555",
                opacity=0.1
            )
        )

        for item in self.packed_items:

            ox_item = item[const.ITEM_X]
            oy_item = item[const.ITEM_Y]
            oz_item = item[const.ITEM_Z]

            extreme_x = item[const.ITEM_LENGTH] + ox_item
            extreme_y = item[const.ITEM_WIDTH] + oy_item
            extreme_z = item[const.ITEM_HEIGHT] + oz_item

            data.append(
                go.Mesh3d(
                    x=[ox_item, ox_item, extreme_x, extreme_x, ox_item, ox_item, extreme_x, extreme_x],
                    y=[oy_item, extreme_y, extreme_y, oy_item, oy_item, extreme_y, extreme_y, oy_item],
                    z=[oz_item, oz_item, oz_item, oz_item, extreme_z, extreme_z, extreme_z, extreme_z],
                    # Intensity of each vertex, which will be interpolated and color-coded
                    # i, j and k give the vertices of triangles
                    i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                    j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
                    k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
                    showscale=True,
                    color=cl.get_random_color(),
                    opacity=1, flatshading=True
                )
            )
            data.append(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers'))

        fig = go.Figure(data)
        fig.update_layout(
            autosize=False,
            width=1300,
            height=900,
            scene_aspectmode='data',
            scene_camera=dict(eye=dict(x=-2, y=-2, z=-1))
        )

        fig.show()

