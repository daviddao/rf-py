from numbapro import autojit
from parse import *
import time

def main():
  
  # Read the bips file from RAxML
  [trees,mxtips,n_tree] = read_bips("bips.txt")
  
  start = time.time()
  # store all dropsets in a file called sets  
  # f = open("drops.txt","w")
  
  # Iterate through all trees
  for i in trees.keys():
    print("calculating dropset for tree",i)
    # Extract the bips
    s_bips = trees[i]['s_bips']
    ind_bips = trees[i]['ind_bips'] 
    s_treeList = trees[i]['sTreeList']
    
    extractTreeDrops(s_bips, ind_bips)  
         
  print("Ok, everything's fine")
  # f.close()
  end = time.time()
  print("Total time needed:",end-start)


@autojit(target="gpu")
def extractTreeDrops(s_bips, ind_bips):
  count = 0 
  maxcount = len(s_bips) * len(ind_bips)
  for s_id, s_bip in enumerate(s_bips):
  # sanity check that we have unambigious bitvector representation
  assert(s_bip[0] == False)

  # look at all possible combinations of ind_bip and s_bip and calculate the dropset
  for ind_id, ind_bip in enumerate(ind_bips):
    # second sanity check
    assert(ind_bip[0] == False)
    count = count + 1
    print("looking at",count,"/",maxcount)
    # calculate dropsets
    drop = calculateDropSet(ind_bip,s_bip)
    # get the global representation of the dropset       
    # drop = [s_treeList[i] for i in indices]
    # sort the dropset for unique representation
    drop = sorted(drop)
        # save tree index and s_bip, ind_bip index
        # f.write(str(i) + " " + str(s_id) + " " + str(ind_id) + "\n")
        # f.write(str(drop) + "\n")

        

'''
Function calculating dropset of two bipartitions in bitvector format
'''
def calculateDropSet(ind_bip,s_bip):

  # calculate the dropsets
  a = ind_bip & s_bip
  b = (~ind_bip) & (~s_bip)
  c = ind_bip & (~s_bip)
  d = (~ind_bip) & s_bip
   
  # choose the dropset representation with smaller bits set
  _ab = a.count() + b.count()
  _cd = c.count() + d.count()
      
  if (_ab > _cd):
    drop = a | b
  else:
    drop = c | d
  
  # now get the indices of bits set to 1 as a list
  indices = np.argwhere(drop == np.amax(drop)).flatten()

  return indices
  
main()
