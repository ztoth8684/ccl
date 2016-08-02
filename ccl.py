"""
	Connected Component Labelling algorithm.
	Jack Lawrence-Jones, July 2016

	For blob/connected component detection. Labels each pixel within a given blob with the same 
	label.
	Monochrome images.

	2 pass implementation using disjoint-set data structure to record label equivalences.
	O(n) for image containing n pixels. 
"""

import copy
import numpy as np
# import Image
from union_find import MakeSet, Union, Find, getNode, display_all_sets


CONNECTIVITY_4 = 1
CONNECTIVITY_8 = 2


def connected_component_labelling(bool_input_image, connectivity_type):
	"""
		2 pass algorithm using disjoint-set data structure to maintain record of label 
		equivalences.

		Input: binary image as 2D boolean array.
		Output: 2D integer array of labelled pixels.

		1st pass: label image and record label equivalence classes.
		2nd pass: replace labels with their root labels.

		(optional 3rd pass: Flatten labels so they are consecutive integers starting from 1.)

	"""
	image_width = len(bool_input_image[0])
	image_height = len(bool_input_image)

	# initialise efficient 2D int array with numpy
	# N.B. numpy matrix addressing syntax: array[y,x]
	labelled_image = np.zeros((image_height, image_width), dtype=np.int16)

	current_label = 1 # Label counter

	# 1st Pass: label image and record label equivalences.
	for y, row in enumerate(bool_input_image): # Pythonic loop index variables
		for x, pixel in enumerate(row):
			
			if pixel == False:
				# Background pixel - leave output pixel value as 0
				pass
			else: 
				# Foreground pixel - work out what its label should be.

				# Get set of neighbour's labels
				labels = neighbouring_labels(labelled_image, connectivity_type, x, y)

				if not labels:
					# If no neighbouring foreground pixels, new label - use current_label 
					labelled_image[y,x] = current_label
					MakeSet(current_label) # record label in disjoint set
					current_label = current_label + 1 # increment for next time				
				
				else:
					# Pixel is definitely part of a connected component: get smallest label of 
					# neighbours
					smallest_label = smallest(labels)
					labelled_image[y,x] = smallest_label

					if len(labels) > 1: # More than one type of label in component -> add 
										# equivalence class.
						for label in labels:
							Union(getNode(smallest_label), getNode(label))


	# 2nd Pass: replace labels with their root labels.
	final_labels = {}
	new_label_number = 1

	for y, row in enumerate(labelled_image):
		for x, pixel_value in enumerate(row):
			
			if pixel_value > 0: # Foreground pixel
				# Get element's set's representative value and use as the pixel's new label.
				new_label = Find(getNode(pixel_value)).value 
				labelled_image[y,x] = new_label

				# Add label to list of labels used, for 3rd pass (flattening label list).
				if new_label not in final_labels.keys():
					final_labels[new_label] = new_label_number
					new_label_number = new_label_number + 1


	# 3rd Pass: flatten label list so labels are consecutive integers starting from 1 (in order 
	# of top to bottom, left to right).
	# Different implementation of disjoint-set may remove the need for 3rd pass?
	for y, row in enumerate(labelled_image):
		for x, pixel_value in enumerate(row):
			
			if pixel_value > 0: # Foreground pixel
				labelled_image[y,x] = final_labels[pixel_value]

	return labelled_image



# Private functions ############################################################################
def neighbouring_labels(image, connectivity_type, x, y):
	"""
		Gets the set of neighbouring labels of pixel(x,y), depending on the connectivity type.

		Labelling kernel (only includes neighbouring pixels that have already been labelled - 
		row above and column to the left):

			Connectivity 4:
				    n
				 w  x  
			 
			Connectivity 8:
				nw  n  ne
				 w  x   
	"""

	labels = set()

	if connectivity_type == CONNECTIVITY_4 or connectivity_type == CONNECTIVITY_8:
		# West neighbour
		if x > 0: # pixel is not on left edge of image
			west_neighbour = image[y,x-1]
			if west_neighbour > 0: # it's a labelled pixel
				labels.add(west_neighbour)

		# North neighbour
		if y > 0: # pixel is not on top edge of image
			north_neighbour = image[y-1,x]
			if north_neighbour > 0: # it's a labelled pixel
				labels.add(north_neighbour)


	if connectivity_type == CONNECTIVITY_8:
		# North-west neighbour
		if x > 0 and y > 0: # pixel is not on left or top edges of image
			northwest_neighbour = image[y-1,x-1]
			if northwest_neighbour > 0: # it's a labelled pixel
				labels.add(northwest_neighbour)

		# North-east neighbour
		if y > 0 and x < len(image[y]) - 1: # pixel is not on top or right edges of image
			northeast_neighbour = image[y-1,x+1]
			if northeast_neighbour > 0: # it's a labelled pixel
				labels.add(northeast_neighbour)

	return labels


def smallest(set_x):
	"""
		Returns the smallest item in the set (returns False if set is empty).
	"""
	if set_x:
		set_x = copy.deepcopy(set_x) # so we don't pop an item off the actual set of labels
		smallest = set_x.pop()
		for item in set_x:
			if item < smallest:
				smallest = item
		return smallest

	else:
		return False


def print_image(image):
	""" 
		Prints a 2D array nicely. For debugging.
	"""
	for y, row in enumerate(image): # python loop index variables
		print(row)



# Testing ######################################################################################
# to do: proper test cases
i1 = [
	[False,False,False,False],
	[False,True,True,True],
	[False,False,False,True],
	[False,True,True,True],
	]

i2 = [
	[1,1,0,0,0,1,1,1,0,0],
	[0,1,0,0,0,0,0,1,0,0],
	[0,0,0,1,0,1,1,1,0,0],
	[0,0,1,1,0,0,0,0,1,0],
	[0,0,1,1,0,0,0,0,0,0],
	[0,1,1,1,0,0,0,1,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,1,1,1,1,1],
	[0,0,0,0,0,1,1,1,1,1],
	[0,0,0,0,0,0,0,0,0,0],
	]

print("Original image:")
print_image(i2)
print("----")

result = connected_component_labelling(i2, CONNECTIVITY_4)
print("Labelled:")
print(result)


# test smallest(set) function
# test_set = set()
# test_set.add(3)
# print(smallest(test_set))
