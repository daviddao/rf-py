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
        # print("extracting line:", count)
        line = f.readline().strip().split(":")
    f.close()

    print("there are ", count, " number of drops!")
    if n > count:
        print("hence, your n is too big!")
    # sort it in reverse order
    keys = sorted(drops, key=float)[::-1]
    print("number of unique keys are", len(keys))
    results = [(k, drops[k]) for k in keys]
    print("Best dropset (score, dropset):")

    count = 0
    for i in range(n):
        if count == n:
            break
        for d_el in results:
            drops = d_el[1]
            for drop in drops:
                # convert the string back into an array
                drop_converted = [int(el) for el in drop[1:-1].split(",")]
                drop_names = translate_to_names(drop_converted, name_file)
                # print(results[i][0], ": ", drop)
                print(d_el[0], ": ", drop_names)
                count += 1
                if count == n:
                    break

    # drop = results[0][1][0]
    # print(drop)
    # drop_converted = [int(el) for el in drop[1:-1].split(",")]
    # drop_names = translate_to_names(drop_converted, name_file)
    # print(results[0][0], drop_names)
    # return drop_names


read_drops("./data/result.txt", "./data/names.txt", 1000)
# read_drops("../data/rogue_results.txt", "../data/rogue_names.txt", )
