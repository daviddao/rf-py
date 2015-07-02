from bitarray import * 

class Tree:

	def __init__(self, idx, global_to_local, local_to_global):
		self.global_to_local = global_to_local
		self.local_to_global = local_to_global
		self.bips = {}
		self.tips = len(local_to_global)
		# keep track which bits are deleted and which are not
		self.valid_bits = bitarray('1' * self.tips)
		self.first = 0

	def get_global_to_local(self):
		return self.global_to_local

	def get_local_to_global(self):
		return self.local_to_global

	def add_bip(self,bip):
		self.bips[bip.to01()] = bip

	def get_bips(self):
		return self.bips

	def get_first(self):
		return self.first

	def set_first(self,i):
		self.first = i

	'''
	returns deleted taxa without affecting the tree valid_bits array directly
	'''
	def delete_taxa(self,indices):
		
		tmp_delete = self.valid_bits.copy()
		# iterate through all indices
		for i in indices:
			tmp_delete[i] = 0

		return tmp_delete

	'''
	if delete first, we use a new index to generate a new bitarray representation
	'''
	def generate_new_representation(self,indices,tmp_delete):

		# TODO: if we delete the first element, we need to re-adjust the representation
		if (self.first in indices):
			# get the index of the first bit set to 1
			new_first = tmp_delete.index(True)
		else:
			new_first = self.get_first()

		bips_dict = self.get_bips()

		for key in bips_dict:
			bip = bips_dict[key]

			new_bitarray = bip.get_bitarray()

			# ok, standard representation needed, we invert everything
			if (new_bitarray[new_first] == 1):
				new_bitarray = ~new_bitarray

			# now it is setted for all!
			bip.set_tmp_bitarray(new_bitarray)


	'''
	1. convert the global deleted indices into local indices
	2. create a new valid_bits bitarray
	3. each bip of the tree checks for itself if it is destroyed
	4. rehash to see if existing, matching ones are going to be merged

	return a penalty score (# destroyed matching bips)
	'''
	def get_penalty(self,g_indices):

		# first convert them to fit our tree
		indices = [self.global_to_local[i] for i in g_indices]

		penalty = 0

		# pseudo delete
		tmp_delete = self.delete_taxa(indices)

		# check if we have to generate a new representation, new representation is stored in tmp_bitarray
		self.generate_new_representation(indices,tmp_delete)

		tmp_dict = {}

		bips_dict = self.get_bips()

		for key in bips_dict:
			bip = bips_dict[key]
			predict_destroyed,new_key = bip.delete_and_check(tmp_delete)

			if (predict_destroyed and bip.get_matching()):
				penalty = penalty + 1

			# rehash the existing ones and look if they already exist and was matching
			if (predict_destroyed == False):
				if ((new_key in tmp_dict) and bip.get_matching()):
					penalty = penalty + 1
				else:
					tmp_dict[new_key] = bip

		return penalty






class Bipartition:

	def __init__(self, idx, bitarray):
		# Save tree number and bipartition id according to bip.txt
		self.idx = idx
		self.bitarray = bitarray
		# used for calculations if the first index is deleted
		self.tmp_bitarray = bitarray
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
		return self.bitarray.copy()

	def get_idx(self):
		return self.idx

	def get_tmp_bitarray(self):
		return self.tmp_bitarray.copy()

	def set_tmp_bitarray(self, tmp_bitarray):
		self.tmp_bitarray = tmp_bitarray


	'''
	Give a deleted_list and test if the bipartition is getting destroyed
	returns:
	True/False - if the bip gets destroyed
	key - the standard representation after deletion
	'''
	def delete_and_check(self,tmp_deleted):

		# Do we actually need to check this bipartition?
		if (self.destroyed == True):
			return "Error, this should have been removed!"

		tmp_bitarray = self.get_tmp_bitarray()
		# we declare leftside always to be the standard representation
		left_side = tmp_bitarray & tmp_deleted 
		right_side = ~tmp_bitarray & tmp_deleted

		# by removing, we destroyed the bipartition
		if ((left_side.count() < 2) or (right_side.count() < 2)):
			return True, left_side.to01()

		return False, left_side.to01()



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

	def get_indices_per_tree(self,taxa_list):
		indices = {}
		# go through all ids in our dropset
		for global_id in self.dropset:
			taxon = taxa_list[global_id]
			tree_ids = taxon.get_trees()

			for tree_id in tree_ids:
				if tree_id in indices:
					indices[tree_id].append(global_id)
				else:
					indices[tree_id] = [global_id]

		return indices



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

		indices_per_tree = self.get_indices_per_tree(taxa_list)

		# for each tree ...
		for tree_id,indices in indices_per_tree.items():
			c_tree = trees[tree_id]["Tree"]

			neg_score = neg_score + c_tree.get_penalty(indices)

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




