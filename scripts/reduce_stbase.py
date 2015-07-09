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
reduce_treefile("../data/stbase.txt", "../data/reduced_stbase.txt", 100000)
