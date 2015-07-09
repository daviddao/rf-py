'''
function translating dropset ids into taxon names
'''


def translate_to_names(list, names):
    f = open(names)
    name_list = f.readline().split()
    dropset_translated = [name_list[ids - 1] for ids in list]
    f.close()
    return dropset_translated
