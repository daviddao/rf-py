from ete2 import Tree

'''
This function takes a set of small trees and delete a list of leaves
'''


def delete(file, target_file, taxa):
    f = open(file)
    t_file = open(target_file, "w")

    count = 0

    for line in f:
        print "looking at tree", count
        line = line.strip().split("=")
        t = Tree(line[1])
        for taxon in taxa:
            leaves = t.get_leaves_by_name(name=taxon)
            for leaf in leaves:
                leaf.delete()

        # prevent falsy trees for RAxML
        while len(t.children) == 1:
            t = t.children[0]

        # write it into the file
        t_file.write(t.write() + "\n")
        count += 1

    f.close()
    t_file.close()

    # TODO: error sorting!

prune = ['Aegilops_sharonensis']
delete("../../data/reduced_stbase.txt", "../../data/pruned_stbase.txt", prune)

'''


Best  20  dropsets (score, dropset):
289 :  ['Aegilops_sharonensis']
287 :  ['Bromus_catharticus', 'Aegilops_sharonensis']
283 :  ['Aegilops_sharonensis', 'Aegilops_ventricosa']
282 :  ['Aegilops_sharonensis', 'Amblyopyrum_muticum']
281 :  ['Aegilops_sharonensis', 'Aegilops_crassa']
279 :  ['Aegilops_sharonensis', 'Aegilops_kotschyi']
275 :  ['Triticum_ispahanicum', 'Aegilops_sharonensis']
267 :  ['Aegilops_sharonensis', 'Aegilops_biuncialis']
240 :  ['Aegilops_sharonensis', 'Aegilops_speltoides']
236 :  ['Aegilops_sharonensis', 'Triticum_timopheevii']
233 :  ['Pseudoroegneria_stipifolia', 'Aegilops_sharonensis']
216 :  ['Aegilops_sharonensis', 'Aegilops_uniaristata']
204 :  ['Triticum_turgidum', 'Aegilops_sharonensis', 'Triticum_timopheevii']
183 :  ['Bromus_catharticus', 'Aegilops_sharonensis', 'Aegilops_speltoides']
177 :  ['Aegilops_sharonensis', 'Aegilops_speltoides', 'Aegilops_ventricosa']
176 :  ['Aegilops_sharonensis', 'Aegilops_speltoides', 'Aegilops_juvenalis']
122 :  ['Aegilops_sharonensis', 'Aegilops_umbellulata']
111 :  ['Solanum_chilense', 'Solanum_peruvianum']
102 :  ['Aegilops_sharonensis', 'Amblyopyrum_muticum', 'Aegilops_umbellulata']
100 :  ['Solanum_incanum', 'Solanum_elaeagnifolium']


Large Tree: 55473, Number of SmallTrees analyzed: 73744
Before Average RF distance 0.271441

Large Tree: 55473, Number of SmallTrees analyzed: 73461
Average RF distance 0.266747


'''
