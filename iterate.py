from calculate_drops import *

## TEST SETS ##
def tests(dropset_dict, trees, taxa_list):
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
  for idx,taxon in enumerate(taxa_list):
    #print(taxon.get_trees())
    print(idx)
    dropsets = taxon.get_dropsets()
    for drops in dropsets:
      print(drops.get_dropset())

  # _dict = trees[10002]['s_bips_dict']
  # for i, key in enumerate(_dict):
  #   bip_e = _dict[key]
  #   e = bip_e.get_matching()
  #   bit = bip_e.get_bitarray()
  #   print(e)

# Main function call
#d_dict, trees, taxa = calculate_drops(False,0,3,"ind_bips.txt")
d_dict, trees, taxa = calculate_drops(False,10001,10020,"bips.txt")
tests(d_dict,trees,taxa)