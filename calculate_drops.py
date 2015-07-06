from parse import *
from Dropset import *
from Tree import *
from Taxon import *
from Bipartition import *
import numpy as np


'''
Function calculating dropset of two bipartitions in bitvector format
'''


def get_drops(ind_bip, s_bip):
    # calculate the dropsets
    a = ind_bip & s_bip
    b = (~ind_bip) & (~s_bip)
    c = ind_bip & (~s_bip)
    d = (~ind_bip) & s_bip

    # choose the dropset representation with smaller bits set
    _ab = a.count() + b.count()
    _cd = c.count() + d.count()

    if _ab < _cd:
        drop = a | b
    else:
        drop = c | d

    # raise flag that we have to deal with a matching dropset
    if drop.count() == 0:
        indices = [-1]
    else:
        # now get the indices of bits set to 1 as a list
        indices = np.argwhere(drop == np.amax(drop)).flatten()

    return indices


'''
Load all bipartitions and calculate the dropset

Parameters:
save - bool, determines if the dropsets are saved in a file called drops.txt
start_tree - index of tree from which we should start extracting bips
end_tree - index of tree till which we extract bips (start_tree < end_tree!)
file - which file should be loaded

returns

- dictionary with all dropsets
- all trees and their bips
- taxa_list containing every taxon and where it appears
'''


def calculate_drops(save, start_tree, end_tree, file):
    # count all dropsets
    drops_count = 0
    comparisons_count = 0

    # Decides if we save dropsets into a file called drops.txt
    save_in_file = save

    # Read the bips file from RAxML (second argument: number of trees)
    [trees, mxtips, n_tree] = read_bips(file, end_tree)

    # Dictionary saving all dropsets
    dropsets_dict = {}
    # Array saving all taxon
    taxa_list = [Taxon(i) for i in range(mxtips + 1)]

    # store all dropsets in a file called sets
    if save_in_file:
        f = open("drops.txt", "w")

    # Iterate through all trees
    # for i in trees.keys():
    for i in range(start_tree, end_tree):
        print("calculating dropset for tree", i)

        # Extract the bips
        s_bips = trees[i]['s_bips']
        ind_bips = trees[i]['ind_bips']
        s_treeList = trees[i]['local_to_global']

        # Save information into Taxon for faster retrieval
        for taxon_id in s_treeList:
            taxa_list[taxon_id].add_tree(i)

        # Dictionary to detect multiple bips
        # trees[i]['s_bips_dict'] = {}
        # s_bips_dict = trees[i]['s_bips_dict']

        # global_to_local maps global to local ids
        trees[i]['global_to_local'] = {}
        g2l_mapping = trees[i]['global_to_local']
        for local_index, global_index in enumerate(s_treeList):
            g2l_mapping[global_index] = local_index

        trees[i]["Tree"] = Tree(i, g2l_mapping, s_treeList)
        tree = trees[i]["Tree"]
        s_bips_dict = tree.get_bips()

        count = 0
        maxcount = len(s_bips) * len(ind_bips)
        comparisons_count += maxcount

        for s_id, s_bip in enumerate(s_bips):
            # sanity check that we have unambigious bitvector representation
            assert (s_bip[0] == False)

            # convert it to string
            key = s_bip.to01()
            # create the bipartition and store it into a dictionary
            s_bip_el = Bipartition((i, s_id), s_bip)
            s_bips_dict[key] = s_bip_el

            # look at all possible combinations of ind_bip and s_bip and calculate the dropset
            for ind_id, ind_bip in enumerate(ind_bips):
                # second sanity check for standard representation
                assert (ind_bip[0] == False)
                count += 1
                # print("looking at",count,"/",maxcount)
                # calculate dropsets and get the indices
                indices = get_drops(ind_bip, s_bip)

                # raised flag, we deal with a matching bipartition
                if indices[0] == -1:
                    s_bip_el.set_matching(True)
                else:

                    # get the global representation of the dropset
                    drop = [s_treeList[i] for i in indices]
                    # sort the dropset for unique key
                    drop = sorted(drop)
                    key = str(drop)

                    # if dropset already exists then get it
                    if key in dropsets_dict:
                        drop_e = dropsets_dict[key]
                        drop_e.add_s_bip(s_bip_el)

                    # otherwise create a new dropset
                    else:
                        drops_count += 1  # one more unique dropset
                        drop_e = Dropset(drop, s_bip_el)
                        dropsets_dict[key] = drop_e

                    # Store the dropset into taxon for easier searching
                    for taxon_id in drop:
                        # Take care not to store duplicates
                        if drop_e not in taxa_list[taxon_id].get_dropsets():
                            taxa_list[taxon_id].add_dropset(drop_e)

                if save_in_file:
                    # save tree index and s_bip, ind_bip index
                    f.write(str(i) + " " + str(s_id) + " " + str(ind_id) + "\n")
                    f.write(str(drop) + "\n")

    print("Ok, everything is fine")
    if save_in_file:
        f.close()
    print("Extracted", drops_count, "unique dropsets from", comparisons_count, "comparisons")

    return dropsets_dict, trees, taxa_list




