import copy
from dataclasses import dataclass

import compute_loading as cl
import constant as const
import numpy as np

from binpacking import Bin, Item


@dataclass
class Packer:
    bins: list[Bin]
    batches: list[list[Item]]

    def pack_into_bin(self, pack_bin, batch):
        item_list = [item.item_in_numpy for item in batch]
        box_size_indices = [const.BIN_LENGTH, const.BIN_WIDTH, const.BIN_HEIGHT]
        item_size_indices = [const.ITEM_LENGTH, const.ITEM_WIDTH, const.ITEM_HEIGHT]
        min_item_size = min([np.min(item[item_size_indices]) for item in item_list])

        remain_batch = []

        wasted_box = []

        for item in item_list:
            if len(pack_bin.free_boxes) == 0:
                break

            forward_boxes = []

            while len(pack_bin.free_boxes) > 0:
                box_index = len(pack_bin.free_boxes) - 1
                if box_index == len(pack_bin.free_boxes) or box_index < 0:
                    break
                new_free_boxes = []

                pack_bin.free_boxes.sort(
                    key=lambda x: -(x[const.BIN_LENGTH] ** 2 - x[const.BIN_HEIGHT])
                )
                box = pack_bin.free_boxes[box_index]

                min_size_current_box = np.min(box[box_size_indices])

                if min_size_current_box < min_item_size:
                    forward_boxes.append(pack_bin.free_boxes.pop(box_index))
                    continue

                if item[const.ITEM_QUANTITY] == 0:
                    forward_boxes.append(pack_bin.free_boxes.pop(box_index))
                    break

                is_small_box = min_size_current_box < np.min(item[item_size_indices])
                fit_in_axis, rotation = cl.rotate_to_max_fit(box, item)
                nb_fit = np.prod(fit_in_axis)

                if is_small_box or nb_fit == 0:
                    forward_boxes.append(pack_bin.free_boxes.pop(box_index))
                    continue

                box_decomposed = cl.decompose_box(box, item)

                for box_dcp in box_decomposed:
                    min_box_size = np.min(box_dcp[box_size_indices])
                    if min_box_size < 1:
                        continue
                    elif min_box_size < min_item_size:
                        wasted_box.append(box_dcp)
                        continue

                    new_free_boxes.append(box_dcp)

                clone_item = np.copy(item)
                clone_item[const.ITEM_QUANTITY] = min(item[const.ITEM_QUANTITY], nb_fit)
                item[const.ITEM_QUANTITY] -= clone_item[const.ITEM_QUANTITY]

                clone_item = cl.rotate(clone_item, rotation)

                packed_items = cl.convert_packed_box_to_item(
                    box, clone_item, fit_in_axis
                )

                for it in packed_items:
                    pack_bin.packed_items.append(it)

                pack_bin.free_boxes.pop(box_index)
                pack_bin.free_boxes.extend(new_free_boxes)

            pack_bin.free_boxes.extend(forward_boxes)

            if item[const.ITEM_QUANTITY] > 0:
                remain_batch.append(Item.from_numpy_array(item))

        return remain_batch

    def pack(self, bin_index, batch_index):
        chosen_bin = self.bins[bin_index]
        batch = self.batches[batch_index]

        remain_batch = self.pack_into_bin(chosen_bin, batch)

        self.batches[batch_index] = remain_batch

    def is_fit_all(self, bin_index, batch_index):
        chosen_bin = copy.deepcopy(self.bins[bin_index])
        batch = copy.deepcopy(self.batches[batch_index])
        remain_batch = self.pack_into_bin(chosen_bin, batch)

        return len(remain_batch) == 0


# packer = Packer(
#     [Bin.from_numpy_array(np.array([10, 10, 10, 0, 0, 0, 0]))],
#     [
#         [
#             Item.from_numpy_array(np.array([2, 3, 4, 40, 0, 0, 0, 0, 0, 1])),
#             Item.from_numpy_array(np.array([1, 1, 2, 20, 0, 0, 0, 0, 1, 1])),
#             Item.from_numpy_array(np.array([2, 2, 2, 20, 0, 0, 0, 0, 2, 1])),
#         ]
#     ],
# )
#
#
# packer.pack(0,0)
#
# # cl.draw_boxes(packer.bins[0].free_boxes)
#
# packer.bins[0].draw_bin()