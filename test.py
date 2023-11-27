import random as rd

import binpacking as bp

data = {}

bins = []
batches = []
for i in range(2):
    bins.append(
        {
            "length": 20,
            "width": 20,
            "height": 15,
            "index": i,
        }
    )

for j in range(3):
    temp = []
    for i in range(3):
        temp.append(
            {
                "length": rd.randint(1, 5),
                "width": rd.randint(1, 5),
                "height": rd.randint(1, 5),
                "quantity": rd.randint(5, 10),
                "index": j * 10 + i,
                "axis_lock": rd.randint(0, 1),
            }
        )
    batches.append(temp)

data["bins"] = bins
data["batches"] = batches
pk = bp.create_packer(data)

a = 1
