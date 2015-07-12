import collections
from calculate_drops import *
import time


'''
RF Opt function taking following arguments:
- start_tree  : first tree to be considered
- end_tree : last tree to be considered
- file : path to the bips.txt, extracted by RAxML
- save (optional) : saving dropsets into a file called drops.txt

returns:
- scoring.txt : a scoring for all dropsets
'''


def rf_optimize(file, target_file, save=False, limit_drops=3):
    one_iteration = True
    start = time.time()
    # Preprocessing
    d_dict, trees, taxa = calculate_drops(save, file, limit_drops)

    # save all trees which should be looked at to enhance performance
    count = 0

    # for key, drops in d_dict.items():
    #     count += 1
    #     print(count)
    #     drops.calculate_indices_per_tree(taxa)

    od = collections.OrderedDict(sorted(d_dict.items()))
    total = len(od)
    iteration = 1
    f = open(target_file, "w")

    while True:

        # use this to save the current mx_score
        mx_score = float('-inf')
        print("Iteration " + str(iteration))
        # f.write("Iteration " + str(iteration) + ":\n")

        # let's test out all dropsets
        count = 0
        for key, drops in od.items():
            # check if its destroyed
            if not drops.destroyed:
                drops.calculate_full_sbips(d_dict)
                [drop, score] = drops.calculate_score(trees, taxa)
                # print(drop, ":", score)
                count += 1
                print(count, "/", total)
                f.write(str(score) + ":" + str(drop) + "\n")

                # if this score is better than the current best
                if mx_score < score:
                    mx_score = score
                    mx_drops = drops

        # emulate do while loop
        if(mx_score < 1 or one_iteration):
            print("end")
            break
        else:
            print("best score: " + str(mx_score))

            mx_drops.calculate_full_sbips(d_dict)
            # we use this to set back all tmp changes
            mx_drops.calculate_score(trees, taxa)
            mx_drops.remove(trees)

            # put the drops here for later checking
            check_drops = []
            check_keys = []
            for taxon_id in mx_drops.get_dropset():
                # get the global taxon
                taxon = taxa[taxon_id]
                for affected_drops in taxon.get_dropset():
                    affected_drops.delete_taxa(taxa, taxon)
                    if not (affected_drops in check_drops):
                        check_keys.append()
                        check_drops.append(affected_drops)

            for c_drop in check_drops:
                pass

            # TODO adjust keys and look for duplicates

            total -= 1

        iteration += 1
    f.close()

    end = time.time()
    print("Total time needed:", end - start)


# rf_optimize(10000, 10020, "data/bips.txt")
rf_optimize("data/r_bips.txt", "data/rogue_results.txt")
# rf_optimize("data/filtered_bips.txt", "data/filtered_results.txt")
