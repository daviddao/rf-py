__author__ = 'David'


class Bipartition:
    def __init__(self, idx, bitarray):
        # Save tree number and bipartition id according to bip.txt
        self.idx = idx
        self.bitarray = bitarray
        # used for calculations if the first index is deleted
        self.tmp_bitarray = bitarray
        self.destroyed = False
        self.tmp_destroyed = False
        self.matching = False
        # the default representation for all bitarrays is always bitvector[0] = 0
        # self.first = 0
        # store a deleted mask
        # self.deleted = bitarray | ~bitarray

    def set_destroy(self, value):
        self.destroyed = value

    def set_matching(self, value):
        self.matching = value

    # print("Yeah, matching!")

    def set_bitarray(self, bitarray):
        self.bitarray = bitarray

    def get_matching(self):
        return self.matching

    def get_bitarray(self):
        return self.bitarray.copy()

    def get_idx(self):
        return self.idx

    def get_tmp_bitarray(self):
        return self.tmp_bitarray.copy()

    def get_tmp_destroyed(self):
        return self.tmp_destroyed

    def set_tmp_bitarray(self, tmp_bitarray):
        self.tmp_bitarray = tmp_bitarray

    '''
    Give a deleted_list and test if the bipartition is getting destroyed
    returns:
    True/False - if the bip gets destroyed
    key - the standard representation after deletion
    '''

    def delete_and_check(self, tmp_deleted):

        # Reset old settings
        self.tmp_destroyed = False

        # Do we actually need to check this bipartition?
        if self.destroyed:
            return "Error, this should have been removed!"

        tmp_bitarray = self.get_tmp_bitarray()
        # we declare leftside always to be the standard representation
        left_side = tmp_bitarray & tmp_deleted
        right_side = ~tmp_bitarray & tmp_deleted

        # by removing, we destroyed the bipartition
        if (left_side.count() < 2) or (right_side.count() < 2):
            return True, left_side.to01()

        return False, left_side.to01()