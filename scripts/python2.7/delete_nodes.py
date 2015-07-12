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
        if len(t) < 3:
            pass
        else:
            # prevent falsy trees for RAxML
            while len(t.children) == 1:
                t = t.children[0]

            # write it into the file
            t_file.write(t.write() + "\n")
        count += 1

    f.close()
    t_file.close()

    # TODO: error sorting!

prune = ['Aegilops_sharonensis', 'Aegilops_speltoides', 'Dasypyrum_villosum']
delete("../../data/filtered_stbase.txt", "../../data/pruned_filtered_stbase.txt", prune)

'''



## This is the result for the filtered set (all trees were 1.0 distance)

411 :  ['Picea_rubens', 'Picea_torano', 'Picea_maximowiczii'] 0.988926, 16571
403 :  ['Picea_rubens', 'Picea_torano'] 0.988953, 16572
400 :  ['Picea_rubens', 'Picea_alcoquiana', 'Picea_torano'] 0.987561, 16567
389 :  ['Picea_breweriana', 'Picea_rubens', 'Picea_torano'] 0.989466, 16545
382 :  ['Picea_rubens', 'Picea_torano', 'Picea_jezoensis'] 0.988573, 16491
350 :  ['Picea_rubens', 'Picea_torano', 'Picea_mariana'] 0.989335, 16482
338 :  ['Picea_glehnii', 'Picea_torano'] 0.996386, 16700
329 :  ['Picea_rubens', 'Picea_koyamae', 'Picea_torano'] 0.989924, 16553
323 :  ['Picea_glauca', 'Picea_rubens', 'Picea_torano'] 0.989704, 16436
315 :  ['Aegilops_sharonensis', 'Aegilops_speltoides', 'Dasypyrum_villosum'] 0.987226, 16146

313 :  ['Aegilops_sharonensis', 'Aegilops_uniaristata', 'Dasypyrum_villosum']
310 :  ['Aegilops_sharonensis', 'Aegilops_speltoides'] 
308 :  ['Hordeum_marinum', 'Aegilops_sharonensis', 'Aegilops_speltoides']
303 :  ['Hordeum_marinum', 'Aegilops_sharonensis', 'Aegilops_uniaristata']
298 :  ['Aegilops_sharonensis', 'Aegilops_uniaristata']
297 :  ['Aegilops_sharonensis', 'Dasypyrum_villosum']
294 :  ['Aegilops_sharonensis', 'Aegilops_speltoides', 'Aegilops_juvenalis']
293 :  ['Hordeum_vulgare', 'Aegilops_sharonensis', 'Aegilops_speltoides']
292 :  ['Aegilops_sharonensis', 'Aegilops_speltoides', 'Aegilops_umbellulata']
291 :  ['Secale_cereale', 'Aegilops_sharonensis', 'Dasypyrum_villosum']

## This is the reduced_stbase

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
