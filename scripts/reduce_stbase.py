from sort_trees import *

'''
function to reduce the trees in stbase
'''


def reduce_treefile(file, targetfile, n):
    f = open(file)
    t_file = open(targetfile, "w")

    count = 0
    for line in f:
        if (count > n):
            t_file.write(line)
        count += 1
    f.close()
    t_file.close()

# ignore 100000 trees
# reduce_treefile("../data/stbase.txt", "../data/reduced_stbase2.txt", 200)

def filter_treefile(file, targetfile, minimumRF):
    f = open(file)
    t_file = open(targetfile, "w")

    # filtered_x = sort_trees(minimumRF)
    filtered_x = get_trees(minimumRF)

    count = 0
    for line in f:
        if count in filtered_x:
            t_file.write(line)
        count += 1
        print(count)

    f.close()
    t_file.close()

filter_treefile("../data/stbase.txt", "../data/0_stbase.txt", 0)