from bitarray import * 

class Bipartition:

	def __init__(self, idx, bitarray):
		# Save tree number and bipartition id according to bip.txt
		self.idx = idx
		self.bitarray = bitarray
		self.destroyed = False
		self.matching = False
		# the default representation for all bitarrays is always bitvector[0] = 0
		self.first = 0
		# store a deleted mask
		self.deleted = bitarray | ~bitarray

	def set_destroy(self,value):
		self.destroyed = value

	def set_matching(self,value):
		self.matching = value
		#print("Yeah, matching!")

	def set_bitarray(self,bitarray):
		self.bitarray = bitarray

	def get_matching(self):
		return self.matching

	def get_bitarray(self):	
		return self.bitarray

	def get_idx(self):
		return self.idx

	'''
	Method removes local_id from a bipartition and test if its getting destroyed
	returns:
	True/False - if the bip gets destroyed
	key - the standard representation after deletion
	'''
	def delete_and_check(self,local_id):

		# Do we actually need to check this bipartition?
		if (self.destroyed == True):
			return "Error, this should have been removed!"

		# copy deletion bitarray and delete the bit
		tmp_deleted = self.deleted.copy()
		tmp_deleted[local_id] = 0

		# TODO: if we delete the first element, we need to re-adjust the representation
		if (local_id == self.first):
			# get the index of the first bit set to 1
			new_first = tmp_deleted.index(True)
		else:
			new_first = self.first

		tmp_bitarray = self.generate_new_representation(new_first)


		# we declare leftside always to be the standard representation
		left_side = tmp_bitarray & tmp_deleted 
		right_side = ~tmp_bitarray & tmp_deleted

		# by removing, we destroyed the bipartition
		if ((left_side.count() < 2) or (right_side.count() < 2)):
			return True, left_side

		return False, left_side


	'''
	uses the index to generate a new bitarray representation
	'''
	def generate_new_representation(self,index):

		new_bitarray = self.bitarray.copy()

		# ok, standard representation needed, we invert everything
		if (new_bitarray[index] == 1):
			new_bitarray = ~new_bitarray

		return new_bitarray



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

	def calculate_score(self,trees,taxa_list):
		# positive score calculated by number of bips in s_bips who were not matching before
		pos_score = 0
		# negative score calculated by all bips which are destroyed and were matching before
		neg_score = 0

		for _bips in self.s_bips:
			_matching = _bips.get_matching()

			# if it wasn't matching before
			if(_matching == False):
				pos_score = pos_score + 1

		# iterate through all taxa in dropset and predict negative score
		for global_id in self.dropset:
			taxon = taxa_list[global_id]
			tree_ids = taxon.get_trees()

			# Now edit all bipartitions of these trees
			check_trees = [trees[i] for i in tree_ids]

			# for each tree ...
			for c_tree in check_trees:
				# save important stuff in variable
				bips_dict = c_tree['s_bips_dict']
				g2l = c_tree['global_to_local']

				# use this dictionary to rehash stuff
				tmp_dict = {}

				# ... get all bips ... 
				for key,bips in bips_dict.items():
					# ... and delete the taxon
					local_id = g2l[global_id]
					predict_destroyed, key = bips.delete_and_check(local_id)

					# if bipartition will be destroyed and was matching before
					if (predict_destroyed and bips.get_matching()):
						neg_score = neg_score + 1

		print(self.get_dropset(),":",pos_score - neg_score)


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




