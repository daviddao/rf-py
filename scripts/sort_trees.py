import operator

'''
Function returning indices of trees with greater than minimumRF
'''

def sort_trees(minimumRF):

    f = open("../data/RAxML_RF-Distances.txt")

    x = {}
    for line in f:
        data = line.strip().split(" ")
        x[int(data[0])] = float(data[1])

    sorted_x = sorted(x.items(), key=operator.itemgetter(1))

    filtered_x = []

    lowest_id = float('inf')
    count = 0
    score = minimumRF
    for el in sorted_x:
        if el[1] >= score:
            if el[0] > 0:
                filtered_x.append(el[0])
                count += 1
                if el[0] < lowest_id:
                    lowest_id = el[0]

    print("number of trees extracted", count)
    print("lowest_id", lowest_id)
    f.close()
    return filtered_x

'''
Function returning indices of trees with only this RF score
'''

def get_trees(RF):

    f = open("../data/RAxML_RF-Distances.txt")

    x = {}
    for line in f:
        data = line.strip().split(" ")
        x[int(data[0])] = float(data[1])

    sorted_x = sorted(x.items(), key=operator.itemgetter(1))

    filtered_x = []

    lowest_id = float('inf')
    count = 0
    score = RF
    for el in sorted_x:
        if el[1] == score:
            if el[0] > 0:
                if el[0] > 100000:
                    filtered_x.append(el[0])
                    count += 1
                    if el[0] < lowest_id:
                        lowest_id = el[0]

    print("number of trees extracted", count)
    print("lowest_id", lowest_id)
    f.close()
    return filtered_x

get_trees(0)


