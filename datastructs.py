import numpy as np 

class Bipartition:

	def __init__(self, bitarray):
		self.bitarray = bitarray
		self.destroyed = False
		self.predictDestroyed = False
		self.matching = False

	def destroy(self):
		self.destroyed = True

	def matching(self):
		self.matching = True	


class Dropset:

	def __init__(self, dropset, tree_id, s_bip_id):
		self.dropset = dropset
		self.s_bips = np.asarray([[tree_id, s_bip_id]])

	# Add a new s_bip
	def add_s_bip(self,tree_id, s_bip_id):
		np.append(self.s_bips,[[tree_id, s_bip_id]],axis=0)

# keeps track of taxon
class Taxon:

	def __init__(self, globalId):
		self.trees = []
		self.dropsets = []
		self.globalId = globalId


