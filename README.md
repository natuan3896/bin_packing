# bin_packing

Read example in example.py

    import random as rd
    import binpacking as bp
    def create_data_model():
        data = {}
        bins = []
        batches = []
        # number of bins
        nb_bin = 2
        # number of batch
        nb_batch = 3
    
        for i in range(nb_bin):
            bins.append(
                {
                    "length": 20,
                    "width": 20,
                    "height": 15,
                    "index": i,
                }
            )
    
        for j in range(nb_batch):
            temp = []
            # number of type of item
            nb_item_type = 3
            for i in range(nb_item_type):
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
    
        # always use 2 key 'bins' and 'batches'
        data["bins"] = bins
        data["batches"] = batches
    
        return data
    # create data for packer
    data = create_data_model()
    
    # create packer
    packer = bp.create_packer(data)
    
    # pack batch 0 into bin 0
    packer.pack(bin_index=0, batch_index=0)
    
    # can draw bin by index to visualize (option)
    packer.draw_bin(bin_index=0)
    
    # Get_output
    result = []
    
    for bin in packer.bins:
        result.append(bin.packed_items_to_dict())

