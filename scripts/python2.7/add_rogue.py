from ete2 import Tree
import random

'''
This function takes a set of small trees and randomly adds a list of rogues
'''


def add_rogue(file, target_file, taxa):
    f = open(file)
    t_file = open(target_file, "w")

    count = 0

    for line in f:
        print "looking at tree", count
        line = line.strip().split("=")
        t = Tree(line[1])
        # A = t.add_child(name="r")
        for taxon in taxa:
            A.add_child(name=taxon)

        # prevent falsy trees for RAxML
        while len(t.children) == 1:
            t = t.children[0]

        # write it into the file
        t_file.write(t.write() + "\n")
        count += 1

    f.close()
    t_file.close()

    # TODO: error sorting!

rogue = ['X']
add_rogue("../../data/0_stbase.txt", "../../data/rogue_stbase.txt", rogue)