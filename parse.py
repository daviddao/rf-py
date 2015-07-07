import numpy as np
from bitarray import bitarray

'''
Parses bipartitions file in form

MASK_LENGTH [NUMBER]
SMALL_TREES_ANALYZED [NUMBER]
LARGE_TREE_SPECIES [NUMBER]
Tree
s_bip_start
[bip_1]
...
[bip_n]
s_bip_end
[local_to_global id mapping]
ind_bip_start
[bip_1]
...
[bip_n]
ind_bip_end

and returns a dictonary containing all bipartitions (induced and smalltrees)
TODO: check if i didn't switch induced and smalltrees
'''


def read_bips(file, treeIter=0):
    f = open(file)
    # Get the mask length for the bitvectors
    mask_length_line = f.readline().split()
    mask_length = int(mask_length_line[1])
    # Get the number of small trees analyzed
    s_trees_count_line = f.readline().split()
    s_trees_count = int(s_trees_count_line[1])
    # Get number of taxa for large tree
    l_tree_species_line = f.readline().split()
    l_tree_species = int(l_tree_species_line[1])

    # Now iterate through all trees
    if treeIter != 0:
        print("selected", treeIter, "trees")
        s_trees_count = treeIter

        # Create a dict to store the bips of each small tree
    # trees = dict.fromkeys(range(s_trees_count))
    trees = [None] * s_trees_count  # Use array instead of dict for slicing, TODO: Speed issues?

    for i in range(s_trees_count):
        print("loading tree", i)
        # Sanity check that now a small tree is coming
        assert (f.readline().split()[0] == "Tree")
        # Extract tree index, number of species and number of splits
        [idx, species, splits] = list(map(int, f.readline().split()))

        # Creating dictionary within dictionary for each tree containing induced bips, small bips and treeList
        trees[i] = dict.fromkeys(["ind_bips", "s_bips", "local_to_global"])
        trees[i]['s_bips'] = np.empty(splits, dtype=object)
        trees[i]['ind_bips'] = np.empty(species - 3, dtype=object)
        trees[i]['local_to_global'] = np.empty(species)

        assert (f.readline().split()[0] == "s_bip_start")
        # Get the next line
        next_line = f.readline().split()
        # We use this variable to sanity check the number of indBips
        count = 0
        # Iterate through all induced bips
        while next_line[0] != "s_bip_end":
            # Extract the bipartition
            s_bip = next_line
            # Convert them into binary format
            s_bip = [np.binary_repr(int(b), width=mask_length)[::-1] for b in s_bip]
            # Create a bitarray
            s_bip = bitarray(''.join(s_bip))
            # Get the offset
            offset = len(s_bip) - species
            # Remove the offset if it exists
            if (offset != 0):
                del s_bip[-offset:]
            # Insert bitarray into ind_bips list
            trees[i]['s_bips'][count] = s_bip
            # increment count afterwards
            count = count + 1
            # lookup the next line
            next_line = f.readline().split()
        assert (count == splits)

        # Get the smallTreeList
        trees[i]['local_to_global'] = list(map(int, f.readline().split()))

        assert (f.readline().split()[0] == "ind_bip_start")
        next_line = f.readline().split()
        count = 0
        # Iterate through all small bips
        while next_line[0] != 'ind_bip_end':
            # Extract the bipartition
            i_bip = next_line
            # Convert them into binary format
            i_bip = [np.binary_repr(int(b), width=mask_length)[::-1] for b in i_bip]
            # Create a bitarray
            i_bip = bitarray(''.join(i_bip))
            offset = len(i_bip) - species
            # Remove the offset
            if (offset != 0):
                del i_bip[-offset:]
            trees[i]['ind_bips'][count] = i_bip
            count += 1
            # lookup next line
            next_line = f.readline().split()

            # We are dealing only with bifurcating large trees, hence their induced tree is also
        # bifurcating
        assert (count == species - 3)
    f.close()
    return trees, l_tree_species, s_trees_count


# [trees,count,species] = read_bips("bips.txt")

# print(trees[0]['s_bips'])
