__author__ = 'David'


# keeps track of which tree, bipartition and co has the taxon
class Taxon:
    def __init__(self, globalId):
        self.trees = []
        self.dropsets = []
        self.globalId = globalId

    def add_tree(self, idx):
        self.trees.append(idx)

    def add_dropset(self, dropset):
        self.dropsets.append(dropset)

    def get_dropsets(self):
        return self.dropsets

    def get_trees(self):
        return self.trees
