from parse import *


def main():
  # Read the bips file from RAxML
  [trees,mxtips,n_tree] = read_bips("bips.txt")

  # Iterate through all trees
  for i in trees.keys():
    print("calculating dropset for tree",i)
    # Extract the bips
    s_bips = trees[i]['s_bips']
    ind_bips = trees[i]['ind_bips'] 
    count = 0 
    maxcount = len(s_bips) * len(ind_bips)
    for s_bip in s_bips:
      # sanity check that we have unambigious bitvector representation
      assert(s_bip[0] == False)
    
      for ind_bip in ind_bips:
        # second sanity check
        assert(ind_bip[0] == False)
        count = count + 1
        print("looking at",count,"/",maxcount)
        # calculate dropsets
        indices = calculateDropSet(ind_bip,s_bip)      
         
  print("Ok, everything's fine")

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
