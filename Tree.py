__author__ = 'David'
from bitarray import *


class Tree:
    def __init__(self, idx, global_to_local, local_to_global):
        self.idx = idx
        self.global_to_local = global_to_local
        self.local_to_global = local_to_global
        self.bips = {}
        self.tips = len(local_to_global)
        # keep track which bits are deleted and which are not
        self.valid_bits = bitarray('1' * self.tips)
        self.first = 0
        self.tmp_first = 0
        # saves the valid bits for the first check iteration
        self.tmp_delete = self.valid_bits.copy()

    def get_global_to_local(self):
        return self.global_to_local

    def get_local_to_global(self):
        return self.local_to_global

    def add_bip(self, bip):
        self.bips[bip.to01()] = bip

    def get_bips(self):
        return self.bips

    def get_first(self):
        return self.first

    def set_first(self, i):
        self.first = i

    '''
    returns deleted taxa without affecting the tree valid_bits array directly
    '''
    def delete_taxa(self, indices):

        self.tmp_delete = self.valid_bits.copy()
        tmp_delete = self.tmp_delete
        # iterate through all indices
        for i in indices:
            tmp_delete[i] = 0

        return tmp_delete

    '''
    if delete first, we use a new index to generate a new bitarray representation
    '''
    def generate_new_representation(self, indices, tmp_delete):

        if self.first in indices:
            # get the index of the first bit set to 1
            new_first = tmp_delete.index(True)
        else:
            new_first = self.get_first()

        # store it temporary
        self.tmp_first = new_first

        bips_dict = self.get_bips()

        for key in bips_dict:
            bip = bips_dict[key]

            new_bitarray = bip.get_bitarray()

            # ok, standard representation needed, we invert everything
            if new_bitarray[new_first] == 1:
                new_bitarray = ~new_bitarray

            # now it is setted for all!
            bip.set_tmp_bitarray(new_bitarray)

    '''
    1. convert the global deleted indices into local indices
    2. create a new valid_bits bitarray
    3. each bip of the tree checks for itself if it is destroyed
    4. rehash to see if existing, matching ones are going to be merged

    return a penalty score (# destroyed matching bips)
    '''
    def get_penalty(self, g_indices):

        # first convert them to fit our tree
        indices = [self.global_to_local[i] for i in g_indices]

        penalty = 0

        # pseudo delete
        tmp_delete = self.delete_taxa(indices)

        bips_dict = self.get_bips()

        # destroyed the whole tree
        if tmp_delete.count() == 0:
            # penalty is the sum of all matching bips in the tree
            for key in bips_dict:
                bip = bips_dict[key]

                if bip.get_matching():
                    penalty += 1

            # exit the code here
            return penalty

        # check if we have to generate a new representation, new representation is stored in tmp_bitarray
        self.generate_new_representation(indices, tmp_delete)

        # use to detect duplicates and mergings in bipartitions
        tmp_dict = {}

        for key in bips_dict:

            # for all bips which are not destroyed
            if not bips_dict[key].destroyed:
                bip = bips_dict[key]
                predict_destroyed, new_key = bip.delete_and_check(tmp_delete)

                if predict_destroyed:
                    # then it is predicted to be destroyed
                    bip.tmp_destroyed = True

                    # if it was matching, this causes a penalty
                    if bip.get_matching():
                        penalty += 1

                # rehash the existing ones and look if they already exist and was matching
                if not predict_destroyed:
                    # two bips are merging, so lets mark one as destroyed
                    if new_key in tmp_dict:
                        bip.tmp_destroyed = True
                        if bip.get_matching():
                            penalty += 1
                    else:
                        tmp_dict[new_key] = bip

        return penalty

    def adapt_changes(self):
        self.valid_bits = self.tmp_delete.copy()
        self.first = self.tmp_first

        for key, bip in self.bips.items():
            # if they are destroyed
            if bip.get_tmp_destroyed():
                bip.destroyed = bip.get_tmp_destroyed()
