from calculate_drops import *
import time

## TEST SETS ##
def tests(dropset_dict, trees, taxa_list):
  pass
  # Check size of drops
  # for i, key in enumerate(dropsets_dict):
  #   drop_e = dropsets_dict[key]
  #   print("Dropset",key)
  #   e = drop_e.get_s_bips()
  #   for bip_e in e:
  #     # All information about the bipartition (tree_id, id, matching)
  #     print(bip_e.get_idx())
  #     print("matching",bip_e.get_matching())

  # Check taxa_list
  # for idx,taxon in enumerate(taxa_list):
  #   print(taxon.get_trees())
  #   print(idx)
  #   print(taxon.get_trees())
    #dropsets = taxon.get_dropsets()
    # for drops in dropsets:
    #   print(drops.get_dropset())


  # Check for local_to_global mapping
  for tree in trees:
    print(tree['Tree'].get_global_to_local())
    print(tree['Tree'].get_local_to_global())
    print(tree['Tree'].delete_taxa([1,3]))

  # _dict = trees[10002]['s_bips_dict']
  # for i, key in enumerate(_dict):
  #   bip_e = _dict[key]
  #   e = bip_e.get_matching()
  #   bit = bip_e.get_bitarray()
  #   print(e)


def rf_optimize(start_tree,end_tree,file,save=False):

  start = time.time()
  # Preprocessing
  d_dict, trees, taxa = calculate_drops(save,start_tree,end_tree,file)
  # Select only some tree
  trees = trees[start_tree:end_tree]

  # We take only positive scores
  mx_score = 0

  # One iteration
  for key,drops in d_dict.items():
    drops.calculate_score(trees,taxa)

  end = time.time()
  print("Total time needed:",end - start)



  #tests(d_dict,trees,taxa)

#rf_optimize(10000,10020,"bips.txt")
#rf_optimize(100000,173431,"bips.txt")
rf_optimize(0,3,"ind_bips.txt")