__author__ = 'David'


class Dropset:
    def __init__(self, dropset, bip):
        # dropset is just an array containing drops
        self.dropset = dropset
        self.s_bips = [bip]
        # Each Dropset has a score
        self.score = 0
        self.destroyed = False

    # Add a new s_bip into an array containing bipartition objects
    def add_s_bip(self, bip):
        self.s_bips.append(bip)

    def get_dropset(self):
        return self.dropset

    def get_s_bips(self):
        return self.s_bips

    def get_score(self):
        return self.score

    def calculate_indices_per_tree(self, taxa_list):
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
        # self.indices_per_tree = indices

    def calculate_score(self, trees, taxa_list):

        # positive score calculated by number of bips in s_bips who were not matching before
        pos_score = 0
        # negative score calculated by all bips which are destroyed and were matching before
        neg_score = 0

        # get the indices from a precalculated stuff
        self.indices_per_tree = self.calculate_indices_per_tree(taxa_list)

        indices_per_tree = self.indices_per_tree

        # for each tree ...
        for tree_id, indices in indices_per_tree.items():
            c_tree = trees[tree_id]["Tree"]

            neg_score = neg_score + c_tree.get_penalty(indices)

        for _bip in self.s_bips:
            _matching = _bip.get_matching()

            # is it is going to be destroyed?
            _destroyed = _bip.get_tmp_destroyed()
            # or is it already destroyed?
            destroyed = _bip.destroyed
            # if it is not destroyed
            if (not _destroyed) and (not destroyed):
                # somehow commenting this yields same results as first algorithm in C
                if not _matching:
                    pos_score += 1

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

    '''
    Remove this dropset will cause an earthquake
    '''
    def remove(self, trees):
        # this dropset is destroyed
        self.destroyed = True

        # set all its s_bips to matching
        for s_bip in self.get_s_bips():
            s_bip.set_matching(True)

        # set all temporary changes in tree to real changes
        for tree_id in self.indices_per_tree:
            t = trees[tree_id]["Tree"]
            t.adapt_changes()

        # TODO: check for merging dropsets and delete their taxa
        # update indices for each dropset

    '''
    Delete taxon and check if dropset is a duplicate
    '''
    def delete_taxa(self, delete_index):
        drops = self.get_dropset()
        delete_key = -1

        for key, taxon in enumerate(drops):
            if taxon == delete_index:
                delete_key = key

        if delete_key >= 0:
            del drops[delete_key]
            # print("Key deleted")
        else: 
            print("Error, negative key given to delete")
