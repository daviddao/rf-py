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


def rf_optimize(start_tree, end_tree, file, save=False):
    start = time.time()
    # Preprocessing
    d_dict, trees, taxa = calculate_drops(save, start_tree, end_tree, file)

    # We take only positive scores
    # mx_score = 0

    f = open("reduced_scoring.txt", "w")
    # One iteration
    od = collections.OrderedDict(sorted(d_dict.items()))
    total = len(od)
    count = 0
    for key, drops in od.items():
        drops.calculate_full_sbips(d_dict)
        [drop, score] = drops.calculate_score(trees, taxa)
        # print(drop, ":", score)
        count += 1
        print(count, "/", total)
        f.write(str(score) + ":" + str(drop) + "\n")
    f.close()

    end = time.time()
    print("Total time needed:", end - start)


# rf_optimize(10000, 10020, "data/bips.txt")
rf_optimize(0, 73744, "data/reduced_bips.txt")
# rf_optimize(0, 3, "data/ind_bips.txt")
