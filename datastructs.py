class Bipartition:

	def __init__(self, idx, bitarray):
		# Save tree number and bipartition id according to bip.txt
		self.idx = idx
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

	def get_idx(self):
		return self.idx

class Dropset:

	def __init__(self, dropset, bip):
		self.dropset = dropset
		self.s_bips = [bip]
		# Each Dropset has a score 
		self.score = 0

	# Add a new s_bip into an array containing bipartition objects
	def add_s_bip(self,bip):
		self.s_bips.append(bip)

	def get_dropset(self):
		return self.dropset

	def get_s_bips(self):
		return self.s_bips

	def get_score(self):
		return self.score

	def calculate_score(self,taxa_list):
		# positive score calculated by number of bips in s_bips who were not matching before
		_pos_score = 0
		# negative score calculated by all bips which are destroyed and were matching before
		_neg_score = 0

		for _bips in self.s_bips:
			_matching = _bips.get_matching()

			# if it wasn't matching before
			if(_matching == False):
				_pos_score = _pos_score + 1

		# iterate through all taxa in dropset and predict negative score
		for _el in self.dropset:
			taxon = taxa_list[_el]




# keeps track of which tree, bipartition and co has the taxon
class Taxon:

	def __init__(self, globalId):
		self.trees = []
		self.dropsets = []
		self.globalId = globalId

	def add_tree(self,idx):
		self.trees.append(idx)

	def add_dropset(self,dropset):
		self.dropsets.append(dropset)

	def get_dropsets(self):
		return self.dropsets

	def get_trees(self):
		return self.trees




