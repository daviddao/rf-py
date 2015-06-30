from parse import *
import time
# Import Dropset Datastructure
from datastructs import *
import numpy as np

# Dictonary saving all dropsets
dropsets_dict = {}

'''
Load all bipartitions and calculate the dropset

Parameters:
save - bool, determines if the dropsets are saved in a file called drops.txt
start_tree - index of tree from which we should start extracting bips
end_tree - index of tree till which we extract bips (start_tree < end_tree!)

'''
def calculate_drops(save,start_tree,end_tree,file):

  # count all dropsets
  drops_count = 0
  comparisons_count = 0
  
  # Decides if we save dropsets into a file called drops.txt
  save_in_file = save

  # Read the bips file from RAxML (second argument: number of trees)
  [trees,mxtips,n_tree] = read_bips(file,end_tree)
  
  start = time.time()
  # store all dropsets in a file called sets
  if (save_in_file):  
  	f = open("drops.txt","w")
  
  # Iterate through all trees
  #for i in trees.keys():
  for i in range(start_tree,end_tree):
    print("calculating dropset for tree",i)

    # Extract the bips
    s_bips = trees[i]['s_bips']
    ind_bips = trees[i]['ind_bips'] 
    s_treeList = trees[i]['sTreeList']

    # Dictonary to detect multiple bips
    trees[i]['s_bips_dict'] = {}
    s_bips_dict = trees[i]['s_bips_dict']

    count = 0 
    maxcount = len(s_bips) * len(ind_bips)
    comparisons_count = comparisons_count + maxcount

    for s_id, s_bip in enumerate(s_bips):
      # sanity check that we have unambigious bitvector representation
      assert(s_bip[0] == False)
      
      # convert it to string
      key = s_bip.to01()
      # create the bipartition and store it into a dictionary
      s_bip_el = Bipartition(s_bip)
      s_bips_dict[key] = s_bip_el


      # look at all possible combinations of ind_bip and s_bip and calculate the dropset
      for ind_id, ind_bip in enumerate(ind_bips):
        # second sanity check
        assert(ind_bip[0] == False)
        count = count + 1
        print("looking at",count,"/",maxcount)
        # calculate dropsets
        indices = get_drops(ind_bip,s_bip)
        # get the global representation of the dropset       
        drop = [s_treeList[i] for i in indices]
        # sort the dropset for unique representation
        drop = sorted(drop)

        key = str(drop)

        # save dropset and its s_bip
        if (key in dropsets_dict):
          drop_e = dropsets_dict[key]
          drop_e.add_s_bip(i,s_id)
        else:
          drops_count = drops_count + 1
          drop_e = Dropset(drop,i,s_id)
          dropsets_dict[key] = drop_e

        if (save_in_file):
        	# save tree index and s_bip, ind_bip index
        	f.write(str(i) + " " + str(s_id) + " " + str(ind_id) + "\n")
        	f.write(str(drop) + "\n")
        
                
         
  print("Ok, everything's fine")
  if (save_in_file):
  	f.close()
  end = time.time()
  print("Total time needed:",end-start)
  print("Extracted",drops_count,"from",comparisons_count,"comparisons")

  # Check size of drops
  for i, key in enumerate(dropsets_dict):
    drop_e = dropsets_dict[key]
    e = drop_e.get_dropset()
    print(i,len(e))
    print(e)

'''
Function calculating dropset of two bipartitions in bitvector format
BUG: same dropset length all the time?
'''
def get_drops(ind_bip,s_bip):

  # calculate the dropsets
  a = ind_bip & s_bip
  b = (~ind_bip) & (~s_bip)
  c = ind_bip & (~s_bip)
  d = (~ind_bip) & s_bip
   
  # choose the dropset representation with smaller bits set
  _ab = a.count() + b.count()
  _cd = c.count() + d.count()

  if (_ab < _cd):
    drop = a | b
  else:
    drop = c | d
  
  # now get the indices of bits set to 1 as a list
  indices = np.argwhere(drop == np.amax(drop)).flatten()

  return indices




# Main function call
calculate_drops(False,0,3,"ind_bips.txt")
