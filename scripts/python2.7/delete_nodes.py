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

        # write it into the file
        t_file.write(t.write() + "\n")

        count += 1

    f.close()
    t_file.close()

prune = ['Picea_rubens', 'Picea_torano']
delete("../../data/reduced_stbase.txt", "../../data/pruned_stbase.txt", prune)


'''
Best  20  dropsets (score, dropset):
99 :  ['Picea_rubens', 'Picea_torano']
96 :  ['Picea_rubens', 'Picea_alcoquiana']
96 :  ['Picea_rubens', 'Picea_maximowiczii']
95 :  ['Picea_rubens', 'Picea_obovata']
95 :  ['Picea_rubens', 'Picea_brachytyla']
95 :  ['Picea_rubens']
90 :  ['Picea_rubens', 'Picea_asperata']
90 :  ['Picea_rubens', 'Picea_neoveitchii']
9 :  ['Eleocharis_vivipara', 'Eleocharis_obtusa']
9 :  ['Eleocharis_vivipara']
9 :  ['Fimbristylis_ferruginea']
9 :  ['Oligostachyum_sulcatum', 'Phyllostachys_nigra', 'Guadua_angustifolia']
9 :  ['Hordeum_arizonicum']
9 :  ['Tasmannia_stipitata']
9 :  ['Loxanthera_speciosa']
9 :  ['Pereskia_lychnidiflora']
9 :  ['Alluaudia_ascendens', 'Didierea_trollii']
9 :  ['Eudianthe_laeta']
9 :  ['Nepenthes_ventricosa', 'Nepenthes_thorelii']
9 :  ['Rheum_palmatum', 'Rheum_rhaponticum', 'Polygonum_chinense']

Before Average RF distance 0.271441

After Average RF distance 0.268303
'''
