#!/usr/bin/python

from __future__ import print_function

import os
import numpy as np
import h5py
import sys

data_dir = r"D:\data\output"
save_path = r"D:\data\output\data.h5"
# data = np.fromfile(sys.argv[1], dtype='float32');
# data = np.reshape(data, (int(sys.argv[2]), int(sys.argv[3])));
# h5f = h5py.File(sys.argv[4], 'w');
# h5f.create_dataset('data', data=data)
# h5f.close()

def train_valid_split(data_dir):
# 	dirname = os.path.dirname(data_dir)
	data_list = list(os.listdir(data_dir))
	male_list = [f for f in data_list if f.startswith('M') and 
										        not f.endswith(".h5")]
	female_list = [f for f in data_list if f.startswith('F') and 
												not f.endswith(".h5")]
	train_list = male_list[:-2] + female_list[:-2]
# 	valid_list = male_list[-4:-2] + female_list[-4:-2]
	test_list = male_list[-2:] + female_list[-2:]
	return [os.path.join(data_dir, f) for f in train_list], \
			[os.path.join(data_dir, f) for f in test_list]
# 			[os.path.join(data_dir, f) for f in valid_list], \


def gen_np_split(data_path_list, nfeatures):
	data_list = list()
	for path in data_path_list:
		data = np.fromfile(path, dtype='float32');
		data = np.reshape(data, (int(data.size/nfeatures), nfeatures))
		data_list.append(data)

	return np.vstack(data_list)

if __name__ == "__main__":
# 	data_dir = sys.argv[1]
# 	save_path = sys.argv[2]
	train_path_list, test_path_list = train_valid_split(data_dir)
	print(train_path_list)

	train_data = gen_np_split(train_path_list, 87)
# 	valid_data = gen_np_split(valid_path_list, 87)
	test_data = gen_np_split(test_path_list, 87)
	print(train_data.shape, test_data.shape)

	h5f = h5py.File(save_path, 'w');
	h5f.create_dataset('train', data=train_data)
# 	h5f.create_dataset('valid', data=valid_data)
	h5f.create_dataset('test', data=test_data)
	h5f.close()



