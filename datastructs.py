import numpy as np 

class Bipartition:

	def __init__(self, bitarray):
		self.bitarray = bitarray
		self.destroyed = False
		self.predictDestroyed = False
		self.matching = False

	def set_destroy(self,value):
		self.destroyed = value

	def set_matching(self,value):
		self.matching = value
		print("Yeah, matching!")

	def set_bitarray(self,bitarray):
		self.bitarray = bitarray

	def get_matching(self):
		return self.matching

	def get_bitarray(self):	
		return self.bitarray

class Dropset:

	def __init__(self, dropset, tree_id, s_bip_id):
		self.dropset = dropset
		self.s_bips = np.asarray([[tree_id, s_bip_id]])

	# Add a new s_bip
	def add_s_bip(self,tree_id, s_bip_id):
		np.append(self.s_bips,[[tree_id, s_bip_id]],axis=0)

	def get_dropset(self):
		return self.dropset

	def get_s_bips(self):
		return self.s_bips

# keeps track of taxon
class Taxon:

	def __init__(self, globalId):
		self.trees = []
		self.dropsets = []
		self.globalId = globalId


