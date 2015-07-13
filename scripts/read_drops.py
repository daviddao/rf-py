from translate_to_names import *


'''
function returning the n highest scoring dropsets
'''


def read_drops(file, name_file, n):
    f = open(file)
    line = f.readline().strip().split(":")
    drops = {}
    count = 1
    # Check for end of file
    while not (line == ['']):
        count += 1
        key = line[0]
        if key in drops:
            drops[key].append(line[1])
        else:
            drops[key] = [line[1]]
        print("extracting line:", count)
        line = f.readline().strip().split(":")
    f.close()

    print("there are ", count, " number of drops!")
    if n > count:
        print("hence, your n is too big!")
    # sort it in reverse order
    keys = sorted(drops, key=float)[::-1]
    results = [(k, drops[k]) for k in keys]
    print("Best ", n, " dropsets (score, dropset):")
    count = 0
    for i in range(n):
        if count == n:
            break
        for d_el in results:
            drop = d_el[1][0]
            # convert the string back into an array
            drop_converted = [int(el) for el in drop[1:-1].split(",")]
            drop_names = translate_to_names(drop_converted, name_file)
            # print(results[i][0], ": ", drop)
            print(d_el[0], ": ", drop_names)
            count += 1
            if count == n:
                break

# read_drops("../data/filtered_results.txt", "../data/names.txt", 20)
read_drops("../data/rogue_results.txt", "../data/rogue_names.txt", 20)
