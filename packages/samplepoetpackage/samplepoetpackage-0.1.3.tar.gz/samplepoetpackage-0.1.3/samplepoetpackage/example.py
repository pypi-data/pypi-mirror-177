"""
File: example.py
------------------
Example python module to test the package install. 
"""

import numpy as np  # test dependency 


def add_two(x):
	return x + 2


def get_shape(some_list):
	x = np.array(some_list)
	return x.shape
	