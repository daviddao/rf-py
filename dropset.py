from parse import *

[trees,mxtips,n_tree] = read_bips("bips.txt")



# Iterate through all trees
for i in trees.keys():
  # Extract the bips
  s_bips = trees[i]['s_bips']
  ind_bips = trees[i]['ind_bips']  
  for idx,s_bip in enumerate(s_bips):
    assert(s_bip[0] == False)
  
  for ind_bip in ind_bips:
    assert(ind_bip[0] == False)
print("Ok, everything's fine")
