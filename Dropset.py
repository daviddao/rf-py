__author__ = 'David'


class Dropset:
    def __init__(self, dropset, bip):
        self.dropset = dropset
        self.s_bips = [bip]
        # Each Dropset has a score
        self.score = 0

    # Add a new s_bip into an array containing bipartition objects
    def add_s_bip(self, bip):
        self.s_bips.append(bip)

    def get_dropset(self):
        return self.dropset

    def get_s_bips(self):
        return self.s_bips

    def get_score(self):
        return self.score

    def get_indices_per_tree(self, taxa_list):
        indices = {}
        # go through all ids in our dropset
        for global_id in self.dropset:
            taxon = taxa_list[global_id]
            tree_ids = taxon.get_trees()

            for tree_id in tree_ids:
                if tree_id in indices:
                    indices[tree_id].append(global_id)
                else:
                    indices[tree_id] = [global_id]

        return indices

    def calculate_score(self, trees, taxa_list):

        check4 = [4]
        if check4 == self.get_dropset():
            pass
        # positive score calculated by number of bips in s_bips who were not matching before
        pos_score = 0
        # negative score calculated by all bips which are destroyed and were matching before
        neg_score = 0

        indices_per_tree = self.get_indices_per_tree(taxa_list)

        # for each tree ...
        for tree_id, indices in indices_per_tree.items():
            c_tree = trees[tree_id]["Tree"]

            neg_score = neg_score + c_tree.get_penalty(indices)

        for _bips in self.s_bips:
            _matching = _bips.get_matching()

            # is it is going to be destroyed?
            _destroyed = _bips.get_tmp_destroyed()

            # if it wasn't matching before
            if not _matching:
                if not _destroyed:
                    pos_score += 1

        if self.get_dropset() == check4:
            print("pos_score", pos_score, "neg_score", neg_score)

        score = pos_score - neg_score

        return self.get_dropset(), score

    '''
    Method to check for all s_bips which are merging due to the removal of multi taxon dropsets
    '''

    def calculate_full_sbips(self, dropsets):

        if len(self.dropset) > 1:
            for taxon in self.dropset:
                # translate to key
                key = [taxon]
                key = str(key)
                if key in dropsets:
                    basic_drop = dropsets[key]
                    # check also for all the s_bips
                    for s_bip in basic_drop.get_s_bips():
                        self.add_s_bip(s_bip)
                else:
                    pass  # no key
        else:
            pass  # elementary dropset